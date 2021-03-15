#! /usr/bin/python3
# -*- coding: utf-8 -*-

from pathlib import Path
from src.epubmeta import EpubMeta
from src.kindlemeta import KindleMeta
from src.mobimeta import MobiMeta


class PathDoesNotExistError(Exception):
    pass

class UnsupportedFormatError(Exception):
    pass

class MetadataFetcher:
    def __init__(self,path):
        self.path = Path(path)
        if self.path.suffix == ".mobi":
            self.meta = MobiMeta(self.path)
        elif self.path.suffix == ".epub":
            self.meta = EpubMeta(self.path)
        elif self.path.suffix in [".azw3","azw","kfx"]:
            self.meta = KindleMeta(self.path)
        else:
            raise UnsupportedFormatError
    def get_metadata(self):
        return self.meta.get_metadata()
    @classmethod
    def get(cls,path):
        meta = cls(path)
        metadata = meta.get_metadata()
        return metadata

def get_metadata(path):
    metadata = MetadataFetcher.get(path)
    return metadata

