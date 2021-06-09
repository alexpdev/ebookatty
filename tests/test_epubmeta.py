#! /usr/bin/python3
# -*- coding: utf-8 -*-

##############################################################################
#     Copyright (C) 2021  alexpdev
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Lesser General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Lesser General Public License for more details.
#
#     You should have received a copy of the GNU Lesser General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
###############################################################################
"""Tests for ebookmeta package."""
from pathlib import Path
from unittest import TestCase
from ebookmeta.epubmeta import EpubMeta

class EpubTest(TestCase):
    """Unittests for primary metadata extractor."""

    def setUp(self):
        """Assign variables used by all tests."""
        self.test_path = Path("./testbooks")



    def test_epub_funcs(self):
        """Test EpubMeta Class."""
        for path in self.test_path.iterdir():
            if path.suffix == ".epub":
                self.assertEqual(path.suffix,".epub")
                meta = EpubMeta(path)
                self.assertTrue(EpubMeta)
                self.assertEqual(meta.suffix,path.suffix)
                self.assertEqual(meta.stem,path.stem)
                self.assertEqual(meta.name,path.name)
                print(meta.metadata)

    def test_metadata(self):
        """Test metadata extracted from EpubMeta Class"""
        for path in self.test_path.iterdir():
            if path.suffix == ".epub":
                meta = EpubMeta(path)
                self.assertTrue(meta.path.exists())
                metadata = meta.get_metadata()
                self.assertIn("filename",metadata)
                self.assertIn("extension",metadata)
                self.assertIn("size",metadata)
                self.assertIn("path",metadata)
                print(metadata)
