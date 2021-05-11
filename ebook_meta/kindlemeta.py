#! /usr/bin/python3
# -*- coding: utf-8 -*-

import struct
from pathlib import Path
from ebook_meta.utils import MetadataError, HeaderMissingError, path_meta
from ebook_meta.standards import EXTH_Types

class KindleMeta:

    types = EXTH_Types

    def __init__(self,path):
        self.path = Path(path)
        self.name = self.path.name
        self.stem = self.path.stem
        self.suffix = self.path.suffix
        self.data = self.path.read_bytes()
        self.palmheader = self.data[:78]
        self.palmname = self.data[:32]
        self.metadata = []
        self.find_metadata()

    def unShort(self,x):
        buffer = self.data
        val = struct.unpack_from(">H", buffer, x)
        return val

    def unLongx(self,total,x):
        buffer = self.data
        form = ">" + ("L"*total)
        val = struct.unpack_from(form, buffer, x)
        return val

    def find_metadata(self):
        """ Find the offset to the EXTH header """
        offset = self.data.find(b'EXTH')
        if offset < 0:
            raise HeaderMissingError(self.path)
        _,headLen,recCount = self.unLongx(3,offset)
        print(headLen)
        offset += 12
        for _ in range(recCount):
            id, size = self.unLongx(2,offset)
            content = self.data[offset + 8 : offset + size]
            record = (id , content)
            self.metadata.append(record)
            offset += size
        if len(self.metadata) < 1:
            raise MetadataError(self.path)

    def get_metadata(self):
        meta = {}
        self.metadata += path_meta(self.path)
        for k,v in self.metadata:
            if hasattr(v,"decode"):
                v = v.decode(errors="replace")
            if k in self.types:
                type_ = self.types[k]
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
