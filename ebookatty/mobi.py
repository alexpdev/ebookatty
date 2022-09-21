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
import re
import struct
from datetime import date
import io
from pathlib import Path
from ebookatty.standards import EXTH_Types

isoformat = date.isoformat

class Metadata:

    def __init__(self):
        self.data = {}

    def setdefault(self, *args):
        self.data.setdefault(*args)

    def __getitem__(self, item):
        if item in self.data:
            return self.data[item]
        else:
            return ['']

    def __setitem__(self, item, other):
        if item in self.data:
            self.data[item].append(other)
        else:
            self.data[item] = [other]

    def add_value(self, key, value):
        self.setdefault(key, [])
        self.data[key].append(value)

    def extend(self, key, value):
        self.setdefault(key, [])
        self.data[key].extend(value)


class EXTHHeader:

    def __init__(self, raw, codec, title, data):
        self._data = data
        self.codec = codec
        self.doctype = raw[:4].decode()
        self.length, self.num_items = struct.unpack('>LL', raw[4:12])
        raw = raw[12:]
        pos = 0
        left = self.num_items
        self.set_data('title', title)
        self.set_data('doctype', self.doctype)
        while left > 0:
            left -= 1
            idx, size = struct.unpack('>LL', raw[pos:pos + 8])
            content = raw[pos + 8:pos + size]
            pos += size
            self.process_metadata(idx, content)

    def decode(self, content):
        return content.decode(self.codec, 'replace').strip()

    def set_data(self, *args):
        self._data.add_value(*args)

    def process_metadata(self, idx, content):
        if idx in EXTH_Types:
            if idx == 100:
                au = self.decode(content)
                m = re.match(r'([^,]+?)\s*,\s+([^,]+)$', au.strip())
                if m is not None:
                    au = m.group()
                self.set_data(EXTH_Types[idx], au)
            elif idx == 105:
                t = [x.strip() for x in self.decode(content).split(';')]
                self._data.extend(EXTH_Types[idx], t)
            elif idx == 112:
                content = self.decode(content)
                isig = 'urn:isbn:'
                if content.lower().startswith(isig):
                    raw = content[len(isig):]
                    if raw:
                        self.set_data('isbn', raw)
                elif content.startswith('calibre:'):
                    cid = content[len('calibre:'):]
                    if cid:
                        self.set_data('uuid', cid)
            else:
                item = self.decode(content)
                if item:
                    self.set_data(EXTH_Types[idx], item)



class BookHeader:

    def __init__(self, raw, data):
        self.raw = raw
        (self.length, self.type, self.codepage,
        self.unique_id, self.version) = struct.unpack('>LLLLL', self.raw[20:40])
        langcode  = struct.unpack('!L', raw[0x5C:0x60])[0]
        data.add_value('type', self.type)
        data.add_value('doctype', self.raw[16:20].decode())
        data.add_value('codepage', self.codepage)
        data.add_value('unique_id', self.unique_id)
        data.add_value('version', self.version)
        data.add_value('langid', langcode & 0xFF)
        data.add_value('version', (langcode >> 10) & 0xFF)
        self.codec = self.get_codec()
        self.title = self.get_title()
        self.exth = self.get_exth(data)

    def get_codec(self):
        if len(self.raw) <= 16 or self.ident == b'TEXTREAD':
            return 'cp1252'
        else:
            return {1252: 'cp1252',
            65001: 'utf-8'}[self.codepage]

    def get_title(self):
        toff, tlen = struct.unpack('>II', self.raw[0x54:0x5c])
        tend = toff + tlen
        title = self.raw[toff:tend] if tend < len(self.raw) else 'Unknown'
        if not isinstance(title, str):
            title = title.decode(self.codec, 'replace')
        return title

    def get_exth(self, data):
        data.add_value('title', self.title)
        data.add_value('codec', self.codec)
        flag, = struct.unpack('>L', self.raw[0x80:0x84])
        if flag & 0x40:
            exth = EXTHHeader(self.raw[16 + self.length:], self.codec,
                self.title, data)
            return exth

class MetadataHeader(BookHeader):

    def __init__(self, stream):
        self.data = Metadata()
        self.stream = stream
        self.stream.seek(0)
        self.ident = self.identity()
        self.data.add_value('identity', self.ident)
        self.num_sections = self.section_count()
        if self.num_sections >= 2:
            header = self.header()
            BookHeader.__init__(self, header, self.data)

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

class Kindle():
    """Gather Epub Metadata."""

    def __init__(self, path):
        """
        Construct the EpubMeta Class Instance.

        Args:
            path (str or pathlike): path to ebook file.
        """
        self.path = Path(path)
        self.stem = self.path.stem
        self.suffix = self.path.suffix
        self.data = self.path.read_bytes()
        self.stream = io.BytesIO(self.data)
        header = MetadataHeader(self.stream)
        metadata = header.data
        metadata.add_value('name', self.stem)
        metadata.add_value('filetype', self.suffix)
        data = metadata.data
        for key, value in data.items():
            value = set(value)
            value = [str(i) for i in value]
            value = '; '.join(value)
            data[key] = value
        self.metadata = data
