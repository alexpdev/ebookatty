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
from ebookmeta.ebookmeta import MetadataFetcher, get_metadata


class EbookMetadataTest(TestCase):
    """Unittests for primary metadata extractor."""

    def setUp(self):
        """Assign variables used by all tests."""
        self.test_path = Path("./testbooks")

    def test_get_metadata(self):
        """Test get_metadata function."""
        for path in self.test_path.iterdir():
            metadata = get_metadata(path)
            self.assertTrue(metadata)
            self.assertIn("filename", metadata)
            self.assertIn("path", metadata)
            self.assertIn("extension", metadata)
            self.assertIn("size", metadata)

    def test_metadata_fetcher(self):
        """Test MetadataFetcher Class."""
        for path in self.test_path.iterdir():
            meta = MetadataFetcher(path)
            metadata = meta.get_metadata()
            self.assertTrue(metadata)
            self.assertIn("filename", metadata)
            self.assertIn("path", metadata)
            self.assertIn("extension", metadata)
            self.assertIn("size", metadata)

    def test_metadata_get(self):
        """Test MetaDataFetcher.get method."""
        for path in self.test_path.iterdir():
            metadata = MetadataFetcher.get(path)
            self.assertTrue(metadata)
            self.assertIn("filename", metadata)
            self.assertIn("path", metadata)
            self.assertIn("extension", metadata)
            self.assertIn("size", metadata)
