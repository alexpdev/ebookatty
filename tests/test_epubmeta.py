import sys
from unittest import TestCase
from os.path import abspath,dirname
sys.path.append(dirname(dirname(abspath(__file__))))
from data.paths import EPUB_BOOKS
from ebook_meta.epubmeta import EpubMeta

class EpubTest(TestCase):

    def setUp(self):
        self.pathiter = EPUB_BOOKS

    def test_epub_funcs(self):
        for path in self.pathiter:
            self.assertEqual(path.suffix,".epub")
            meta = EpubMeta(path)
            self.assertTrue(EpubMeta)
            self.assertEqual(meta.suffix,path.suffix)
            self.assertEqual(meta.stem,path.stem)
            self.assertEqual(meta.name,path.name)
            print(meta.metadata)

    def test_metadata(self):
        for path in self.pathiter:
            path = abspath(path)
            meta = EpubMeta(path)
            self.assertTrue(meta.path.exists())
            metadata = meta.get_metadata()
            self.assertIn("filename",metadata)
            self.assertIn("extension",metadata)
            self.assertIn("size",metadata)
            self.assertIn("path",metadata)
            print(metadata)
