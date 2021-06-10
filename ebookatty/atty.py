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
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#########################################################################
"""
Metadata Parsing and extracting from ebook files.

ebookatty module.
"""
import sys
from argparse import ArgumentParser
from pathlib import Path

from ebookatty.epubmeta import EpubMeta
from ebookatty.kindlemeta import KindleMeta
from ebookatty.mobimeta import MobiMeta


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
        if self.path.suffix == ".mobi":
            self.meta = MobiMeta(self.path)
        elif self.path.suffix == ".epub":
            self.meta = EpubMeta(self.path)
        elif self.path.suffix in [".azw3", "azw", "kfx"]:
            self.meta = KindleMeta(self.path)
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
    ]
    longest_line = 0
    longest_field = max([len(i) for i in fields])
    for field in fields:
        if field in book:
            extra_spaces = longest_field - len(field)
            line = (" " * extra_spaces) + "\t" + str(book[field][0]) + "\n"
            line = field.title() + line
            output += line
            if len(line) > longest_line:
                longest_line = len(line)
    output += "-" * longest_line + "\n"
    return output
