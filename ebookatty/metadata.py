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
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from ebookatty import mobi, epub

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
            self.epubmeta = epub.get_epub_info(str(self.path), self.path.name, self.path.suffix)
            self.meta = Epub(self.path)
        elif self.path.suffix in [".azw3", "azw", "kfx", ".mobi"]:
            self.meta = mobi.Kindle(self.path)
        else:
            raise UnsupportedFormatError

    def get_metadata(self):
        """
        Call to start the extraction process.

        Returns:
            dict: Metadata keys and values embedded in the file.
        """
        try:
            data = self.meta.get_metadata()
        except:
            data = self.meta.metadata
        return data

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
            line = (" " * extra_spaces) + "\t" + str(book[field]) + "\n"
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
