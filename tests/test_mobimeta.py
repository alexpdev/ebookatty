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
"""Tests for MobiMeta module."""

from pathlib import Path
from unittest import TestCase

from ebookatty.mobimeta import MobiMeta


class MobiTest(TestCase):
    """Unittests for primary metadata extractor."""

    def setUp(self):
        """Assign variables used by all tests."""
        path = Path("./testbooks")
        books = [i for i in path.iterdir() if i.suffix == ".mobi"]
        self.books = books

    def test_mobi_funcs(self):
        """Test MobiMeta Class."""
        for path in self.books:
            self.assertEqual(path.suffix, ".mobi")
            mobimeta = MobiMeta(path)
            self.assertTrue(MobiMeta)
            self.assertEqual(mobimeta.suffix, path.suffix)
            self.assertEqual(mobimeta.stem, path.stem)
            self.assertEqual(mobimeta.name, path.name)
            self.assertEqual(mobimeta.data, path.read_bytes())
            self.assertTrue(mobimeta.metadata)
            print(mobimeta.metadata)

    def test_metadata(self):
        """Test metadata extracted from MobiMeta Class"""
        for path in self.books:
            meta = MobiMeta(path)
            self.assertTrue(meta.path.exists())
            metadata = meta.get_metadata()
            self.assertIn("filename", metadata)
            self.assertIn("extension", metadata)
            self.assertIn("path", metadata)
            self.assertIn("size", metadata)
            print(metadata)
