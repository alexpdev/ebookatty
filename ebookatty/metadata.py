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
import io
from pathlib import Path
from xml.etree import ElementTree as ET
from ebookatty.standards import EXTH_Types, language, _OPF_PARENT_TAGS

class Metadata:

    def __init__(self):
        self.rights = None
        self.tags = []
        self.language = None
        self.title = None
        self.authors = []
        self.author_sort = None
        self.publisher = None
        self.comments = []
        self.isbn = None
        self.pubdate = None
        self.book_producer = None
        self.application_id = None
        self.uuid = None

    def set_identifier(self, ident, val):
        if ident not in self.__dict__:
            self.__dict__[ident] = val
        else:
            self.__dict__[ident] = val

class EXTHHeader:

    def __init__(self, raw, codec, title):
        self.doctype = raw[:4]
        self.length, self.num_items = struct.unpack('>LL', raw[4:12])
        raw = raw[12:]
        pos = 0
        self.mi = Metadata()
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
                try:
                    self.cdetype = content.decode('ascii')
                except UnicodeDecodeError:
                    self.cdetype = None
                if content == b'EBSP':
                    if not self.mi.tags:
                        self.mi.tags = []
                    self.mi.tags.append('Sample Book')
            elif idx == 503:
                try:
                    title = content.decode(codec)
                except UnicodeDecodeError:
                    pass
            elif idx == 524:
                try:
                    lang = content.decode(codec)
                    if lang:
                        self.mi.language = lang
                except UnicodeDecodeError:
                    pass
            elif idx == 525:
                try:
                    pwm = content.decode(codec)
                    if pwm:
                        self.primary_writing_mode = pwm
                except Exception:
                    pass
            elif idx == 527:
                try:
                    ppd = content.decode(codec)
                    if ppd:
                        self.page_progression_direction = ppd
                except Exception:
                    pass
        if title:
            self.mi.title = title

    def decode(self, content):
        return content.decode()

    def process_metadata(self, idx, content, codec):
        if idx == 100:
            if self.mi.is_null('authors'):
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
            if self.mi.publisher in {'Unknown', b'Unknown'}:
                self.mi.publisher = None
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
            try:
                self.mi.pubdate = self.decode(content)
            except Exception:
                pass
        elif idx == 108:
            self.mi.book_producer = self.decode(content).strip()
        elif idx == 109:
            self.mi.rights = self.decode(content).strip()
        elif idx == 112:
            try:
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
            except:
                pass
        elif idx == 113:
            try:
                self.uuid = content.decode('ascii')
                self.mi.set_identifier('mobi-asin', self.uuid)
            except Exception:
                self.uuid = None
        elif idx == 116:
            self.start_offset, = struct.unpack(b'>L', content)
        elif idx == 121:
            self.kf8_header, = struct.unpack(b'>L', content)
            if self.kf8_header == 0xffffffff:
                self.kf8_header = None

class BookHeader:

    def __init__(self, raw, ident, user_encoding, try_extra_data_fix=False):
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
            self.doctype = raw[16:20]
            self.length, self.type, self.codepage, self.unique_id, \
                self.version = struct.unpack('>LLLLL', raw[20:40])

            try:
                self.codec = {
                    1252: 'cp1252',
                    65001: 'utf-8',
                    }[self.codepage]
            except (IndexError, KeyError):
                self.codec = 'cp1252' if not user_encoding else user_encoding
            max_header_length = 500
            if (ident == b'TEXTREAD' or self.length < 0xE4 or
                    self.length > max_header_length or
                    (try_extra_data_fix and self.length == 0xE4)):
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
                    if self.exth.mi.is_null('language'):
                        try:
                            self.exth.mi.language = langid
                        except:
                            pass
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


class MetadataHeader(BookHeader):

    def __init__(self, stream):
        self.stream = stream
        self.ident = self.identity()
        self.num_sections = self.section_count()
        if self.num_sections >= 2:
            header = self.header()
            BookHeader.__init__(self, header, self.ident, None)
        else:
            self.exth = None

    @property
    def kf8_type(self):
        if (self.mobi_version == 8 and getattr(self, 'skelidx', 0xffffffff) !=
                0xffffffff):
            return 'standalone'

        kf8_header_index = getattr(self.exth, 'kf8_header', None)
        if kf8_header_index is None:
            return None
        try:
            if self.section_data(kf8_header_index-1) == b'BOUNDARY':
                return 'joint'
        except Exception:
            pass
        return None

    def identity(self):
        self.stream.seek(60)
        ident = self.stream.read(8).upper()
        if ident not in (b'BOOKMOBI', b'TEXTREAD'):
            raise Exception
        return ident

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

    def section_data(self, number):
        start = self.section_offset(number)
        if number == self.num_sections -1:
            end = os.stat(self.stream.name).st_size
        else:
            end = self.section_offset(number + 1)
        self.stream.seek(start)
        try:
            return self.stream.read(end - start)
        except OverflowError:
            self.stream.seek(start)
            return self.stream.read()

    def __str__(self):
        return f'{self.__dict__}, {self.exth.mi.__dict__}'


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
        self.ident = self.identity()
        self.title = self.name()
        self.num_sections = self.section_count()
        self.palmheader = self.data[:78]
        self.palmname = self.data[:32]
        self.metadata = []
        self.find_metadata()

    def identity(self):
        self.stream.seek(60)
        ident = self.stream.read(8)
        return ident.decode('utf-8')

    def section_count(self):
        self.stream.seek(76)
        return struct.unpack('>H', self.stream.read(2))[0]

    def name(self):
        self.stream.seek(0)
        pattern = re.compile(b'[^-A-Za-z0-9 ]+')
        return pattern.sub(b'_', self.stream.read(32).replace(b'\x00', b''))

    def unShort(self, x):
        """
        Convert bits to text.

        Args:
            x (bytes): bytes to decode

        Returns:
            str: decoded bytes
        """
        buffer = self.data
        val = struct.unpack_from(">H", buffer, x)
        return val

    def unLongx(self, total, x):
        """
        Convert bits to text.

        Args:
            total (int): number of bytes to decode
            x (bytes): bytes to decode

        Returns:
            str: decoded bytes
        """
        buffer = self.data
        form = ">" + ("L" * total)
        val = struct.unpack_from(form, buffer, x)
        return val

    def find_metadata(self):
        header = MetadataHeader(self.stream)
        meta = {}
        for k,v in header.__dict__.items():
            if v:
                meta[k] = v
        for k,v in header.exth.mi.__dict__.items():
            if v:
                meta[k] = v
        for key in ['stream', 'exth']:
            del meta[key]
        return meta


class Epub:
    """Gather Epub Metadata."""

    def __init__(self, path):
        """
        Construct the EpubMeta Class Instance.

        Args:
            path (str or pathlike): path to ebook file.
        """
        self.tags = [
            "dc:title",
            "dc:contributor",
            "dc:creator",
            "dc:identifier",
            "dc:language",
            "dc:publisher",
            "dc:date",
            "dc:description",
            "dc:subject",
            "dc:rights",
            "creator",
            "publisher",
            "title",
            "language",
            "description",
            "subject",
        ]
        self.path = Path(path)
        self.name = self.path.name
        self.stem = self.path.stem
        self.suffix = self.path.suffix
        self.zipfile = zipfile.ZipFile(self.path)
        self.metadata = []
        self.find_metadata()

    def __str__(self):
        """
        Format to string representation.

        Returns:
            str: string representation of instance.
        """
        return f"EpubMeta({str(self.path)})"

    def get_opf(self):
        """
        Get the .opf file within the ebook archive.

        Raises:
            MetadataError: If it cannot parse metadata file

        Returns:
            (str): the path to the .opf file.
        """
        for fname in self.zipfile.namelist():
            if fname.endswith(".opf"):
                return fname
        raise MetadataError

    def find_metadata(self):
        """
        Find metadata within the ebook archive file.

        Returns:
            dict: key,value pairs for ebook metadata
        """
        with self.zipfile as zfile:
            opf_file = self.get_opf()
            with zfile.open(opf_file, "r") as zfile:
                ztext = zfile.read()
                self.xpath_parse(ztext)
                self.pattern_parse(ztext)
        return self.metadata

    def pattern_parse(self, opf):
        """
        Parse .opf file for Metadata using regex. and xpath.

        Args:
            opf (str):  path to opf file
        """
        text = str(opf)
        metadata = []
        for tag in self.tags:
            pat1 = re.compile(f"<{tag}.*?>(.*)</{tag}", re.S | re.M)
            result = pat1.search(text)
            if result:
                groups = result.groups()
                if isinstance(groups, str):
                    record = (tag, groups)
                    metadata.append(record)
                else:
                    for group in groups:
                        record = (tag, group)
                        metadata.append(record)
        self.metadata += metadata

    def xpath_parse(self, opf):
        """
        Parse .opf file with xpath selectors.

        Args:
            opf (str): path to opf file to parse
        """
        root = ET.fromstring(opf)
        ns = {
            "dc": "http://purl.org/dc/elements/1.1/",
            "opf": "http://www.idpf.org/2007/opf",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "dcterms": "http://purl.org/dc/terms/",
        }
        metadata = []
        for tag in self.tags:
            matches = root.findall(tag, ns)
            records = [(tag, match.text) for match in matches]
            metadata += records
        self.metadata += metadata

    def get_metadata(self):
        """
        Extract and format metadata into a dictionary.

        Returns:
            dict: key,value pairs of metadata extracted.
        """
        self.metadata += path_meta(self.path)
        meta = {}
        for k, v in self.metadata:
            if "dc:" in k:
                k = k[3:]
            if k in meta:
                meta[k].append(v)
            else:
                meta[k] = [v]
        return meta

class PathDoesNotExistError(Exception):
    """
    Raise when ebook path does not exist.

    Args:
        Exception (Obj): Raises an Exception
    """

    pass


class UnsupportedFormatError(Exception):
    """
    Raise when ebook file format is unsupported.

    Args:
        Exception (Obj): Raises an Exception
    """

    pass


class MetadataFetcher:
    """Primary Entrypoint for extracting metadata from most ebook filetypes."""

    def __init__(self, path):
        """
        Construct the MetadataFetcher Class and return Instance.

        Args:
            path (str or path-like): The path to the ebook to extract from

        Raises:
            UnsupportedFormatError: When unknown format is encountered
        """
        self.path = Path(path)
        if self.path.suffix == ".epub":
            self.meta = Epub(self.path)
        elif self.path.suffix in [".azw3", "azw", "kfx", ".mobi"]:
            self.meta = Kindle(self.path)
        else:
            raise UnsupportedFormatError

    def get_metadata(self):
        """
        Call to start the extraction process.

        Returns:
            dict: Metadata keys and values embedded in the file.
        """
        return self.meta.get_metadata()

    @classmethod
    def get(cls, path):
        """
        Get metadata from ebook at specified path.

        Args:
            path (str or path-like): Path to ebook.

        Returns:
            dict: Metadata keys and values embedded in the file.
        """
        meta = cls(path)
        metadata = meta.get_metadata()
        print(format_output(metadata))
        return metadata


def get_metadata(path):
    """
    Extract metadata from ebooks.

    Args:
        path (str or path-like): Path to ebook file.

    Returns:
        dict: Metadata keys and values embedded in the file.
    """
    metadata = MetadataFetcher.get(path)
    return metadata


def format_output(book):
    """
    Format the output for printing to STDOUT.

    Args:
        book (str or path-like): Path to ebook file

    Returns:
        str: Text data to output to STDOUT
    """
    output = ""
    fields = [
        "filename",
        "path",
        "extension",
        "size",
        "author",
        "title",
        "publisher",
        "creator",
        "language",
        "contributor",
        "date",
        "rights",
        "tags",
        "authors",
        "author_sort",
        "comments",
        "isbn",
        "pubdate",
        "book_producer",
        "application_id",
        "uuid",
        "codec",
        "doctype",
        "sublanguage",
        "unique_id",
        "ident"
    ]
    longest_line = 0
    longest_field = max([len(i) for i in fields])
    for field in fields:
        if field in book:
            extra_spaces = longest_field - len(field)
            line = (" " * extra_spaces) + "\t" + str(book[field][0]) + "\n"
            line = field.title() + line
            output += line
            if len(line) + 1 > longest_line:
                longest_line = len(line) + 1
    output += "-" * longest_line + "\n"
    output = "-" * longest_line + "\n" + output
    return output


class HeaderMissingError(Exception):
    """Raise HeaderMissingError."""

    pass


class MetadataError(HeaderMissingError):
    """Raise MetadataError."""

    pass


def path_meta(path):
    """
    Metadata extracted from the file and path names.

    Args:
        path (str): path to file

    Returns:
        dict: key, value pairs of metadata parsed.
    """
    if isinstance(path, str):
        path = Path(path)
    metadata = [
        ("filename", path.name),
        ("path", str(path)),
        ("extension", path.suffix),
        ("size", path.stat().st_size),
    ]
    return metadata


def reverse_tag_iter(block):
    """
    Decode tag names.

    Args:
        block (bytes): tag names

    Yields:
        str: tag name
    """
    end = len(block)
    while True:
        pgt = block.rfind(b">", 0, end)
        if pgt == -1:
            break
        plt = block.rfind(b"<", 0, pgt)
        if plt == -1:
            break
        yield block[plt : pgt + 1]
        end = plt


def getLanguage(langID, sublangID):
    """
    Get Language Standard.

    Args:
        langID (str): Landguage ID
        sublangID (str): Sublanguage ID

    Returns:
        str: Language encoding.
    """
    sublangID = 0 if not sublangID else sublangID
    try:
        lang = language[langID][sublangID]
    except KeyError:
        lang = "en"
    return lang
