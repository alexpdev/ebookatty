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
from pathlib import Path
import shutil
from xml.etree import ElementTree as ET
from ebookatty import mobi, epub, standards

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
            self.meta = epub.Epub(self.path)
        elif self.path.suffix in [".azw3", "azw", "kfx", ".mobi"]:
            self.meta = mobi.Kindle(self.path)

    def get_metadata(self):
        """
        Call to start the extraction process.

        Returns:
            dict: Metadata keys and values embedded in the file.
        """
        data = self.meta.metadata
        print(format_output(data))
        return data

def format_output(book):
    """
    Format the output for printing to STDOUT.

    Args:
        book (str or path-like): Path to ebook file

    Returns:
        str: Text data to output to STDOUT
    """
    fields = standards.ALL_TAGS
    termsize = shutil.get_terminal_size().columns
    long_tag = max([len(key) for key in book.keys()])
    tail_size = termsize - long_tag - 5
    long_line = 0
    output = []
    for key, value in book.items():
        if key not in fields:
            continue
        if "\n" in value:
            value = " ".join(value.split("\n"))
        left = long_tag - len(key)
        start = key + ":" + (" " * left)
        if len(value) <= tail_size:
            start += "\t" + value
            if len(start) > long_line:
                long_line = len(start)
            output.append(start)
        else:
            long_line = termsize - 3
            sections = text_sections(tail_size, value)
            extra = (" " * len(start)) + "\t"
            text = start + "\t" + next(sections) + "\n"
            for section in sections:
                text += extra + section + "\n"
            output.append(text)
    output.insert(0,"\n" +("-" * long_line))
    output.append(("-" * long_line) + "\n")
    final = "\n".join(output)
    print(final)

def text_sections(section_size, text):
    while len(text) > section_size:
        size = section_size
        while text[size] != ' ':
            size -= 1
        yield text[:size]
        text = text[size+1:]
    yield text
