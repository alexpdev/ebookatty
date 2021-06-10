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
import struct
from pathlib import Path

from ebookatty.utils import HeaderMissingError, MetadataError, path_meta
from ebookatty.standards import EXTH_Types



class KindleMeta:
    """Gather Epub Metadata."""

    def __init__(self, path):
        """
        Construct the EpubMeta Class Instance.

        Args:
            path (str or pathlike): path to ebook file.
        """
        self.path = Path(path)
        self.name = self.path.name
        self.stem = self.path.stem
        self.suffix = self.path.suffix
        self.data = self.path.read_bytes()
        self.palmheader = self.data[:78]
        self.palmname = self.data[:32]
        self.metadata = []
        self.find_metadata()

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
        """Find the offset to the EXTH header."""
        offset = self.data.find(b"EXTH")
        if offset < 0:
            raise HeaderMissingError(self.path)
        _, headLen, recCount = self.unLongx(3, offset)
        offset += 12
        for _ in range(recCount):
            id, size = self.unLongx(2, offset)
            content = self.data[offset + 8 : offset + size]
            record = (id, content)
            self.metadata.append(record)
            offset += size
        if len(self.metadata) < 1:
            raise MetadataError(self.path)

    def get_metadata(self):
        """
        Extract metadata from ebook.

        Returns:
            dict: key, value pairs of metadata.
        """
        meta = {}
        self.metadata += path_meta(self.path)
        for k, v in self.metadata:
            if hasattr(v, "decode"):
                v = v.decode(errors="replace")
            if k in EXTH_Types:
                type_ = EXTH_Types[k]
                if type_ not in meta:
                    meta[type_] = [v]
                else:
                    meta[type_].append(v)
            else:
                if str(k) not in meta:
                    meta[str(k)] = [v]
                else:
                    meta[str(k)].append(v)
        return meta
