#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path
from os.path import dirname,abspath
from argparse import ArgumentParser
sys.path.append(dirname(dirname(abspath(__file__))))
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

def format_output(book):
    output = ""
    fields = ["filename","path","extension","size","author","title","publisher","creator","language","contributor","date"]
    longest_line = 0
    longest_field = max([len(i) for i in fields])
    for field in fields:
        if field in book:
            extra_spaces = longest_field - len(field)
            line = field.title() + (" "*extra_spaces) + "\t" + str(book[field][0]) + "\n"
            output += line
            if len(line) > longest_line:
                longest_line = len(line)
    output += "-"*longest_line + "\n"
    return output


def cliparse(args):
    parser = ArgumentParser(description="get ebook metadata")
    parser.add_argument("-f","--file",nargs="+",help="path to ebook")
    parser.add_argument("-d","--directory",action='append',help="path to ebooks directory")
    paths = parser.parse_args(sys.argv)
    if paths.file:
        for fname in paths.file:
            print(format_output(get_metadata(fname)))
    if paths.directory:
        d = [Path(i) for i in paths.directory]
        for path in d:
            for item in path.iterdir():
                print(format_output(get_metadata(item)))
    print(paths,dir(paths))


if __name__ == "__main__":
    cliparse(sys.argv[1:])
