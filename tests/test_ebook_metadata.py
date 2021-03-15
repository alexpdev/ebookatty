import sys
from unittest import TestCase
from os.path import abspath,dirname
sys.path.append(dirname(dirname(abspath(__file__))))
from data.paths import PATH
from src.ebook_metadata import MetadataFetcher,get_metadata

class EbookMetadataTest(TestCase):

    def setUp(self):
        self.path = PATH
        self.pathiter = (i for i in PATH.iterdir() if i.suffix in [".azw3",".epub",".kfx",".mobi"])
    
    def test_ebook_formats(self):
        pass

    def test_get_metadata(self):
        for path in self.pathiter:
            metadata = get_metadata(path)
            self.assertTrue(metadata)
            self.assertIn("filename",metadata)
            self.assertIn("path",metadata)
            self.assertIn("extension",metadata)
            self.assertIn("size",metadata)

    def test_metadata_fetcher(self):
        for path in self.pathiter:
            meta = MetadataFetcher(path)
            metadata = meta.get_metadata()
            self.assertTrue(metadata)
            self.assertIn("filename",metadata)
            self.assertIn("path",metadata)
            self.assertIn("extension",metadata)
            self.assertIn("size",metadata)

    def test_metadata_get(self):
        for path in self.pathiter:
            metadata = MetadataFetcher.get(path)
            self.assertTrue(metadata)
            self.assertIn("filename",metadata)
            self.assertIn("path",metadata)
            self.assertIn("extension",metadata)
            self.assertIn("size",metadata)


