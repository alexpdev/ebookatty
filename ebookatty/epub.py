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
"""Epub module for extracting metadata from ebooks with the .epub extension."""

import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from ebookatty.standards import OPF_TAGS


class Epub:
    """
    Representation of structured ebook metadata.

    Parameters
    ----------
    path : str
        path to the ebook file.
    """

    def __init__(self, path: str):
        """
        Construct the Epub Class Instance.
        """
        self.tags = OPF_TAGS
        self.path = Path(path)
        self.epub_zip = zipfile.ZipFile(self.path)
        self.stem = self.path.stem
        self.suffix = self.path.suffix
        self.opf = self.get_opf()
        self.opf_data = self.epub_zip.read(self.opf).decode()
        root = ET.fromstring(self.opf_data)
        meta = self.iterer(root)
        for key, val in meta.items():
            if val:
                val = '; '.join([str(i) for i in set(val)])
                if val == "en":
                    val = "English"
                meta[key] = val
        if "creator" in meta:
            meta["author"] = meta["creator"]
        self.metadata = meta

    def iterer(self, root: ET.Element) -> dict:
        """
        Iterate through elements looking for metadata tags.

        Recursively iterate through each and every element checking it's tag
        and attributes for metadata information and assigning the values to a
        metadata dictionary and returning the final compiled result.

        Parameters
        ----------
        root : ET.Element
            the root element to iterate

        Returns
        -------
        dict
            all metadata extracted from element and its children
        """
        pattern = re.compile(r'\{.*\}(\w+)')
        match = pattern.findall(root.tag)[0]
        if match in self.tags and root.text not in [None, "None", "NONE"]:
            meta = {match: [root.text]}
        else:
            meta = {}
        for element in root:
            if element != root:
                data = self.iterer(element)
                for k,v in data.items():
                    meta.setdefault(k,[])
                    meta[k].extend(v)
        return meta

    def get_opf(self) -> str:
        """
        Extract the path to the zipfile opf file.

        The OPF file contains all of the metadata that needs to be extracted.

        Returns
        -------
        str
            the absolute path to the opf file contained in the ziparchive
        """
        ns = {'n': 'urn:oasis:names:tc:opendocument:xmlns:container',
              'pkg': 'http://www.idpf.org/2007/opf',
              'dc': 'http://purl.org/dc/elements/1.1/'}
        txt = self.epub_zip.read('META-INF/container.xml')
        tree = ET.fromstring(txt)
        elems = tree.findall('n:rootfiles/n:rootfile', namespaces=ns)
        for elem in elems:
            if 'full-path' in elem.attrib:
                return elem.attrib['full-path']
        return None
