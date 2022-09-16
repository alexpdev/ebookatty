#! /usr/bin/python3
# -*- coding: utf-8 -*-

########################################################################
#  Copyright (C) 2021  alexpdev
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#########################################################################
"""
Module contains implementation specific to amazon formatted ebooks.

Classes and functions for .azw, .azw3, and .kfx ebooks.
"""

import os
import re
import struct
import zipfile
from datetime import date
import io
import copy
from pathlib import Path
from ebookatty.standards import SIMPLE_GET, SIMPLE_SET, TOP_LEVEL_IDENTIFIERS, STANDARD_METADATA_FIELDS, ALL_METADATA_FIELDS
from xml.etree import ElementTree as ET
from ebookatty.standards import EXTH_Types, _OPF_PARENT_TAGS

isoformat = date.isoformat

ck = lambda typ: typ.lower().strip().replace(':', '').replace(',', '')
cv = lambda val: val.strip().replace(',', '|')

NULL_VALUES = {
                'user_metadata': {},
                'cover_data'   : (None, None),
                'tags'         : [],
                'identifiers'  : {},
                'languages'    : [],
                'device_collections': [],
                'author_sort_map': {},
                'authors'      : ['Unknown'],
                'author_sort'  : 'Unknown',
                'title'        : 'Unknown',
                'user_categories' : {},
                'author_link_map' : {},
                'language'     : 'und'
}

def string_to_authors(raw):
    if not raw:
        return []
    raw = raw.replace('&&', '\uffff')
    _author_pat = re.compile(r'(?i),?\s+(and|with)\s+')
    raw = _author_pat.sub('&', raw)
    authors = [a.strip().replace('\uffff', '&') for a in raw.split('&')]
    return [a for a in authors if a]

def authors_to_string(authors):
    if authors is not None:
        return ' & '.join([a.replace('&', '&&') for a in authors if a])
    else:
        return ''

class Metadata:
    __calibre_serializable__ = True

    def __init__(self, title, authors=('Unknown',), other=None):
        _data = copy.deepcopy(NULL_VALUES)
        _data.pop('language')
        object.__setattr__(self, '_data', _data)
        if other is not None:
            self.smart_update(other)
        else:
            if title:
                self.title = title
            if authors:
                # List of strings or []
                self.author = list(authors) if authors else []  # Needed for backward compatibility
                self.authors = list(authors) if authors else []

    def is_null(self, field):
        try:
            null_val = NULL_VALUES.get(field, None)
            val = getattr(self, field, None)
            return not val or val == null_val
        except:
            return True

    def set_null(self, field):
        null_val = copy.copy(NULL_VALUES.get(field))
        setattr(self, field, null_val)

    def __getattribute__(self, field):
        _data = object.__getattribute__(self, '_data')
        if field in SIMPLE_GET:
            return _data.get(field, None)
        if field in TOP_LEVEL_IDENTIFIERS:
            return _data.get('identifiers').get(field, None)
        if field == 'language':
            try:
                return _data.get('languages', [])[0]
            except:
                return NULL_VALUES['language']
        return object.__getattribute__(self, field)

    def __setattr__(self, field, val, extra=None):
        _data = object.__getattribute__(self, '_data')
        if field in SIMPLE_SET:
            if val is None:
                val = copy.copy(NULL_VALUES.get(field, None))
            _data[field] = val
        elif field in TOP_LEVEL_IDENTIFIERS:
            field, val = self._clean_identifier(field, val)
            identifiers = _data['identifiers']
            identifiers.pop(field, None)
            if val:
                identifiers[field] = val
        elif field == 'identifiers':
            if not val:
                val = copy.copy(NULL_VALUES.get('identifiers', None))
            self.set_identifiers(val)
        elif field == 'language':
            langs = []
            if val and val.lower() != 'und':
                langs = [val]
            _data['languages'] = langs
        else:
            # You are allowed to stick arbitrary attributes onto this object as
            # long as they don't conflict with global or user metadata names
            # Don't abuse this privilege
            self.__dict__[field] = val

    def __iter__(self):
        return iter(object.__getattribute__(self, '_data'))

    def has_key(self, key):
        return key in object.__getattribute__(self, '_data')

    def deepcopy(self, class_generator=lambda : Metadata(None)):
        ''' Do not use this method unless you know what you are doing, if you
        want to create a simple clone of this object, use :meth:`deepcopy_metadata`
        instead. Class_generator must be a function that returns an instance
        of Metadata or a subclass of it.'''
        m = class_generator()
        if not isinstance(m, Metadata):
            return None
        object.__setattr__(m, '__dict__', copy.deepcopy(self.__dict__))
        return m

    def deepcopy_metadata(self):
        m = Metadata(None)
        object.__setattr__(m, '_data', copy.deepcopy(object.__getattribute__(self, '_data')))
        return m

    def get(self, field, default=None):
        try:
            return self.__getattribute__(field)
        except AttributeError:
            return default


    def set(self, field, val, extra=None):
        self.__setattr__(field, val, extra)

    def get_identifiers(self):
        '''
        Return a copy of the identifiers dictionary.
        The dict is small, and the penalty for using a reference where a copy is
        needed is large. Also, we don't want any manipulations of the returned
        dict to show up in the book.
        '''
        ans = object.__getattribute__(self,
            '_data')['identifiers']
        if not ans:
            ans = {}
        return copy.deepcopy(ans)

    def _clean_identifier(self, typ, val):
        if typ:
            typ = ck(typ)
        if val:
            val = cv(val)
        return typ, val

    def set_identifiers(self, identifiers):
        '''
        Set all identifiers. Note that if you previously set ISBN, calling
        this method will delete it.
        '''
        cleaned = {ck(k):cv(v) for k, v in iter(identifiers.items()) if k and v}
        object.__getattribute__(self, '_data')['identifiers'] = cleaned

    def set_identifier(self, typ, val):
        'If val is empty, deletes identifier of type typ'
        typ, val = self._clean_identifier(typ, val)
        if not typ:
            return
        identifiers = object.__getattribute__(self,
            '_data')['identifiers']

        identifiers.pop(typ, None)
        if val:
            identifiers[typ] = val

    def has_identifier(self, typ):
        identifiers = object.__getattribute__(self,
            '_data')['identifiers']
        return typ in identifiers

    # field-oriented interface. Intended to be the same as in LibraryDatabase

    def standard_field_keys(self):
        '''
        return a list of all possible keys, even if this book doesn't have them
        '''
        return STANDARD_METADATA_FIELDS

    def all_non_none_fields(self):
        '''
        Return a dictionary containing all non-None metadata fields, including
        the custom ones.
        '''
        result = {}
        _data = object.__getattribute__(self, '_data')
        for attr in STANDARD_METADATA_FIELDS:
            v = _data.get(attr, None)
            if v is not None:
                result[attr] = v
        # separate these because it uses the self.get(), not _data.get()
        for attr in TOP_LEVEL_IDENTIFIERS:
            v = self.get(attr, None)
            if v is not None:
                result[attr] = v
        return result

    def authors_from_string(self, raw):
        self.authors = string_to_authors(raw)


    def __unicode__representation__(self):
        '''
        A string representation of this object, suitable for printing to
        console
        '''
        ans = []

        def fmt(x, y):
            ans.append('%-20s: %s'%(str(x), str(y)))

        fmt('Title', self.title)
        if self.title_sort:
            fmt('Title sort', self.title_sort)
        if self.authors:
            fmt('Author(s)',  authors_to_string(self.authors) +
               ((' [' + self.author_sort + ']')
                if self.author_sort and self.author_sort != 'Unknown' else ''))
        if self.publisher:
            fmt('Publisher', self.publisher)
        if getattr(self, 'book_producer', False):
            fmt('Book Producer', self.book_producer)
        if self.tags:
            fmt('Tags', ', '.join([str(t) for t in self.tags]))
        if self.series:
            fmt('Series', self.series + ' #%s'%self.format_series_index())
        if not self.is_null('languages'):
            fmt('Languages', ', '.join(self.languages))
        if self.rating is not None:
            fmt('Rating', ('%.2g'%(float(self.rating)/2)) if self.rating
                    else '')
        if self.timestamp is not None:
            fmt('Timestamp', isoformat(self.timestamp))
        if self.pubdate is not None:
            fmt('Published', isoformat(self.pubdate))
        if self.rights is not None:
            fmt('Rights', str(self.rights))
        if self.identifiers:
            fmt('Identifiers', ', '.join(['%s:%s'%(k, v) for k, v in
                iter(self.identifiers.items())]))
        if self.comments:
            fmt('Comments', self.comments)

        for key in self.custom_field_keys():
            val = self.get(key, None)
            if val:
                (name, val) = self.format_field(key)
                fmt(name, str(val))
        return '\n'.join(ans)

    def to_html(self):
        ans = [(('Title'), str(self.title))]
        ans += [(('Author(s)'), (authors_to_string(self.authors) if self.authors else ('Unknown')))]
        ans += [(('Publisher'), str(self.publisher))]
        ans += [(('Producer'), str(self.book_producer))]
        ans += [(('Comments'), str(self.comments))]
        ans += [('ISBN', str(self.isbn))]
        ans += [(('Tags'), ', '.join([str(t) for t in self.tags]))]
        if self.series:
            ans += [(('Series', 'Series', 1), str(self.series) + ' #%s'%self.format_series_index())]
        ans += [(('Languages'), ', '.join(self.languages))]
        if self.timestamp is not None:
            ans += [(('Timestamp'), str(isoformat(self.timestamp, as_utc=False, sep=' ')))]
        if self.pubdate is not None:
            ans += [(('Published'), str(isoformat(self.pubdate, as_utc=False, sep=' ')))]
        if self.rights is not None:
            ans += [(('Rights'), str(self.rights))]
        for key in self.custom_field_keys():
            val = self.get(key, None)
            if val:
                (name, val) = self.format_field(key)
                ans += [(name, val)]
        for i, x in enumerate(ans):
            ans[i] = '<tr><td><b>%s</b></td><td>%s</td></tr>'%x
        return '<table>%s</table>'%'\n'.join(ans)

    __str__ = __unicode__representation__

    def __nonzero__(self):
        return bool(self.title or self.author or self.comments or self.tags)
    __bool__ = __nonzero__


class EXTHHeader:

    def __init__(self, raw, codec, title):
        self.doctype = raw[:4]
        self.length, self.num_items = struct.unpack('>LL', raw[4:12])
        raw = raw[12:]
        pos = 0
        self.mi = Metadata(title)
        self.has_fake_cover = True
        self.start_offset = None
        left = self.num_items
        self.kf8_header = None
        self.uuid = self.cdetype = None
        self.page_progression_direction = None
        self.primary_writing_mode = None
        while left > 0:
            left -= 1
            idx, size = struct.unpack('>LL', raw[pos:pos + 8])
            content = raw[pos + 8:pos + size]
            pos += size
            if idx >= 100 and idx < 200:
                self.process_metadata(idx, content, codec)
            elif idx == 203:
                self.has_fake_cover = bool(struct.unpack('>L', content)[0])
            elif idx == 201:
                co, = struct.unpack('>L', content)
                if co < 0xffffffff:
                    self.cover_offset = co
            elif idx == 202:
                self.thumbnail_offset, = struct.unpack('>L', content)
            elif idx == 501:
                self.cdetype = content.decode('ascii')
            elif idx == 503:
                title = content.decode(codec)
            elif idx == 524:
                lang = content.decode(codec)
                if lang:
                    self.mi.language = lang
            elif idx == 525:
                pwm = content.decode(codec)
                if pwm:
                    self.primary_writing_mode = pwm
            elif idx == 527:
                ppd = content.decode(codec)
                if ppd:
                    self.page_progression_direction = ppd
        if title:
            self.mi.title = title

    def decode(self, content):
        return content.decode()

    def process_metadata(self, idx, content, codec):
        if idx == 100:
            if not self.mi.authors:
                self.mi.authors = []
            au = self.decode(content).strip()
            m = re.match(r'([^,]+?)\s*,\s+([^,]+)$', au.strip())
            if m is not None:
                self.mi.authors.append(m.group())
                if not self.mi.author_sort:
                    self.mi.author_sort = m.group()
                else:
                    self.mi.author_sort += ' & ' + m.group()
            else:
                self.mi.authors.append(au)
        elif idx == 101:
            self.mi.publisher = self.decode(content).strip()
        elif idx == 103:
            self.mi.comments  = self.decode(content).strip()
        elif idx == 104:
            raw = self.decode(content).strip().replace('-', '')
            if raw:
                self.mi.isbn = raw
        elif idx == 105:
            if not self.mi.tags:
                self.mi.tags = []
            self.mi.tags.extend([x.strip() for x in self.decode(content).split(';')])
            self.mi.tags = self.mi.tags[:]
        elif idx == 106:
            self.mi.pubdate = self.decode(content)
        elif idx == 108:
            self.mi.book_producer = self.decode(content).strip()
        elif idx == 109:
            self.mi.rights = self.decode(content).strip()
        elif idx == 112:
            content = content.decode(codec).strip()
            isig = 'urn:isbn:'
            if content.lower().startswith(isig):
                raw = content[len(isig):]
                if raw and not self.mi.isbn:
                    self.mi.isbn = raw
            elif content.startswith('calibre:'):
                cid = content[len('calibre:'):]
                if cid:
                    self.mi.application_id = self.mi.uuid = cid
        elif idx == 113:
            self.uuid = content.decode('ascii')
            self.mi.set_identifier('mobi-asin', self.uuid)
        elif idx == 116:
            self.start_offset, = struct.unpack(b'>L', content)
        elif idx == 121:
            self.kf8_header, = struct.unpack(b'>L', content)
            if self.kf8_header == 0xffffffff:
                self.kf8_header = None

class BookHeader:

    def __init__(self, raw, ident):
        self.compression_type = raw[:2]
        self.records, self.records_size = struct.unpack('>HH', raw[8:12])
        self.encryption_type, = struct.unpack('>H', raw[12:14])
        if ident == b'TEXTREAD':
            self.codepage = 1252
        if len(raw) <= 16:
            self.codec = 'cp1252'
            self.extra_flags = 0
            self.title = 'Unknown'
            self.language = 'ENGLISH'
            self.sublanguage = 'NEUTRAL'
            self.exth_flag, self.exth = 0, None
            self.ancient = True
            self.first_image_index = -1
            self.mobi_version = 1
        else:
            self.ancient = False
            self.doctype = raw[16:20].decode()
            self.length, self.type, self.codepage, self.unique_id, \
                self.version = struct.unpack('>LLLLL', raw[20:40])

            try:
                self.codec = {
                    1252: 'cp1252',
                    65001: 'utf-8',
                    }[self.codepage]
            except (IndexError, KeyError):
                self.codec = 'cp1252'
            max_header_length = 500
            if (ident == b'TEXTREAD' or self.length < 0xE4 or self.length > max_header_length):
                self.extra_flags = 0
            else:
                self.extra_flags, = struct.unpack('>H', raw[0xF2:0xF4])

            if self.compression_type == b'DH':
                self.huff_offset, self.huff_number = struct.unpack('>LL',
                        raw[0x70:0x78])

            toff, tlen = struct.unpack('>II', raw[0x54:0x5c])
            tend = toff + tlen
            self.title = raw[toff:tend] if tend < len(raw) else 'Unknown'
            langcode  = struct.unpack('!L', raw[0x5C:0x60])[0]
            langid    = langcode & 0xFF
            sublangid = (langcode >> 10) & 0xFF
            self.language =  'ENGLISH'
            self.sublanguage =  'NEUTRAL'
            self.mobi_version = struct.unpack('>I', raw[0x68:0x6c])[0]
            self.first_image_index = struct.unpack('>L', raw[0x6c:0x6c + 4])[0]

            self.exth_flag, = struct.unpack('>L', raw[0x80:0x84])
            self.exth = None
            if not isinstance(self.title, str):
                self.title = self.title.decode(self.codec, 'replace')
            if self.exth_flag & 0x40:
                try:
                    self.exth = EXTHHeader(raw[16 + self.length:], self.codec,
                            self.title)
                    self.exth.mi.uid = self.unique_id
                    if not self.exth.mi.language:
                        self.exth.mi.language = langid
                except:
                    self.exth_flag = 0

            self.ncxidx = 0xffffffff
            if len(raw) >= 0xF8:
                self.ncxidx, = struct.unpack_from(b'>L', raw, 0xF4)

            if self.mobi_version == 8 and len(raw) >= (0xF8 + 16):
                self.dividx, self.skelidx, self.datpidx, self.othidx = \
                        struct.unpack_from(b'>4L', raw, 0xF8)
                self.fdstidx, self.fdstcnt = struct.unpack_from(b'>2L', raw, 0xC0)
                if self.fdstcnt <= 1:
                    self.fdstidx = 0xffffffff
            else:
                self.skelidx = self.dividx = self.othidx = self.fdstidx = \
                        0xffffffff


from ebookatty.standards import mobi8_header
class MetadataHeader(BookHeader):

    def __init__(self, stream):
        self.stream = stream
        self.ident = self.identity()
        self.num_sections = self.section_count()
        if self.num_sections >= 2:
            header = self.header()
            self.unpack(header)
            BookHeader.__init__(self, header, self.ident)

    def unpack(self, header):
        metadata = {}
        for k,v in mobi8_header.items():
            metadata[k] = struct.unpack(v[1], header[v[0]:v[0]+v[2]])


    def identity(self):
        self.stream.seek(60)
        ident = self.stream.read(8).upper()
        return ident.decode()

    def section_count(self):
        self.stream.seek(76)
        return struct.unpack('>H', self.stream.read(2))[0]

    def section_offset(self, number):
        self.stream.seek(78 + number * 8)
        return struct.unpack('>LBBBB', self.stream.read(8))[0]

    def header(self):
        section_headers = []
        section_headers.append(self.section_offset(0))
        section_headers.append(self.section_offset(1))
        end_off = section_headers[1]
        off = section_headers[0]
        self.stream.seek(off)
        return self.stream.read(end_off - off)


def get_metadata(stream):
    stream.seek(0)
    mh = MetadataHeader(stream)
    return mh

class Kindle:
    """Gather Epub Metadata."""

    def __init__(self, path):
        """
        Construct the EpubMeta Class Instance.

        Args:
            path (str or pathlike): path to ebook file.
        """
        self.path = Path(path)
        # self.name = self.path.name
        self.stem = self.path.stem
        self.suffix = self.path.suffix
        self.data = self.path.read_bytes()
        self.stream = io.BytesIO(self.data)
        self.palmheader = self.data[:78]
        self.palmname = self.data[:32]
        self.header = get_metadata(self.stream)
        self.metadata = {}
        for k,v in self.header.__dict__.items():
            if not isinstance(v, (str, int, float, list, tuple, set, dict)):
                continue
            self.metadata[k] = v
        for k,v in self.header.exth.mi.__dict__.items():
            if not isinstance(v, (str, int, float, list, tuple, set, dict)):
                continue
            self.metadata[k] = v
