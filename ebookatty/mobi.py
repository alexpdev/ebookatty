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
    """
    Metadata representations for EXTH headers and other various fields.
    """

    def __init__(self):
        """Constructor for the metadata object."""
        self.data = {}

    def setdefault(self, *args: tuple) -> None:
        """Set the default value for key, same as the dict.setdefault."""
        self.data.setdefault(*args)

    def __getitem__(self, item: str):
        """
        Get the value associated with the attribute provided.

        Parameters
        ----------
        item : str
            name of the attribute

        Returns
        -------
        Any
            the value associated with the attribute
        """
        if item in self.data:
            return self.data[item]
        else:
            return ['']

    def __setitem__(self, item: str, other):
        """
        Set the item of the attribute value to the value.

        Parameters
        ----------
        item : str
            Name of the attribute
        other : Any
            the value to set the attribute to
        """
        if item in self.data:
            self.data[item].append(other)
        else:
            self.data[item] = [other]

    def add_value(self, key: str, value: str) -> None:
        """
        Adds the value and key to the data dictionary.

        Parameters
        ----------
        key : str
            the name of the attribute
        value : str
            the value to set the attribute to
        """
        self.setdefault(key, [])
        self.data[key].append(value)

    def extend(self, key: str, value: list) -> None:
        """
        Extend the value of the key with the contents of the list.

        Parameters
        ----------
        key : str
            name of the field
        value : list
            contents to extend
        """
        self.setdefault(key, [])
        self.data[key].extend(value)


class EXTHHeader:
    """
     Header class for EXTH metadata fields.
    """

    def __init__(self, raw: bytes, codec: str, title: str, data: Metadata):
        """
        Constructor for the EXTH header class.

        Parameters
        ----------
        raw : bytes
            the raw data
        codec : str
            the text encoding format string
        title : str
            title of the book
        data : Metadata
            metadata holder class
        """
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

    def decode(self, content: bytes) -> str:
        """
        Decode raw bytes to string.

        Parameters
        ----------
        content : bytes
            the raw byte content to decode

        Returns
        -------
        str
            decoded bytes
        """
        return content.decode(self.codec, 'replace').strip()

    def set_data(self, *args) -> None:
        """
        Call the set_data method of the Metadata object.
        """
        self._data.add_value(*args)

    def process_metadata(self, idx: int, content: bytes):
        """
        Extract the appropriate metadata associated with the field.

        Parameters
        ----------
        idx : int
            the index of the record content
        content : bytes
            raw byte data of the record
        """
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
    """
    Metadata header for the ebook.
    """

    def __init__(self, raw: bytes, data: Metadata):
        """
        Construct the metadata header.

        Parameters
        ----------
        raw : bytes
            header section of the ebook
        data : Metadata
            dictionary holding the metadata
        """
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

    def get_codec(self) -> str:
        """
        Extract the string encoding for the header records.

        Returns
        -------
        str
            encoding string
        """
        if len(self.raw) <= 16 or self.ident == b'TEXTREAD':
            return 'cp1252'
        else:
            return {1252: 'cp1252',
            65001: 'utf-8'}[self.codepage]

    def get_title(self) -> str:
        """
        Get the title metadata field.

        Returns
        -------
        str
            Ebook title.
        """
        toff, tlen = struct.unpack('>II', self.raw[0x54:0x5c])
        tend = toff + tlen
        title = self.raw[toff:tend] if tend < len(self.raw) else 'Unknown'
        if not isinstance(title, str):
            title = title.decode(self.codec, 'replace')
        return title

    def get_exth(self, data: bytes) -> Metadata:
        """
        Extract the exth header fields from ebook.

        Parameters
        ----------
        data : bytes
            Exth header section

        Returns
        -------
        Metadata
            instance of Metadata class
        """
        data.add_value('title', self.title)
        data.add_value('codec', self.codec)
        flag, = struct.unpack('>L', self.raw[0x80:0x84])
        if flag & 0x40:
            exth = EXTHHeader(self.raw[16 + self.length:], self.codec,
                self.title, data)
            return exth

class MetadataHeader(BookHeader):
    """
    MetadataHeader class.
    """

    def __init__(self, stream: io.BytesIO):
        """
        Construct the MetadataHeader instance.

        Parameters
        ----------
        stream : io.BytesIO
            ebook byte stream
        """
        self.data = Metadata()
        self.stream = stream
        self.stream.seek(0)
        self.ident = self.identity()
        self.data.add_value('identity', self.ident)
        self.num_sections = self.section_count()
        if self.num_sections >= 2:
            header = self.header()
            BookHeader.__init__(self, header, self.data)

    def identity(self) -> str:
        """
        Extract identity metadata field.

        Returns
        -------
        str
            identity metadata field.
        """
        self.stream.seek(60)
        ident = self.stream.read(8).upper()
        return ident.decode()

    def section_count(self) -> int:
        """
        Count the sections in the header.

        Returns
        -------
        int
            number of sections
        """
        self.stream.seek(76)
        return struct.unpack('>H', self.stream.read(2))[0]

    def section_offset(self, number: int) -> int:
        """
        Extract the offset location for the header.

        Parameters
        ----------
        number : int
            value of offset

        Returns
        -------
        int
            value of next records
        """
        self.stream.seek(78 + number * 8)
        return struct.unpack('>LBBBB', self.stream.read(8))[0]

    def header(self) -> bytes:
        """
        Return precise section of the ebook that makes the header.

        Returns
        -------
        bytes
            raw data for ebook header
        """
        section_headers = []
        section_headers.append(self.section_offset(0))
        section_headers.append(self.section_offset(1))
        end_off = section_headers[1]
        off = section_headers[0]
        self.stream.seek(off)
        return self.stream.read(end_off - off)

class Kindle():
    """Gather Epub Metadata."""

    def __init__(self, path: str):
        """
        Construct the EpubMeta Class Instance.

        Parameters
        ----------
        path : str
            path to ebook file.
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
