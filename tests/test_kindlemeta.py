import sys
from unittest import TestCase
from os.path import abspath,dirname
sys.path.append(dirname(dirname(abspath(__file__))))
from data.paths import KINDLE_BOOKS
from ebook_meta.kindlemeta import KindleMeta

class KindleTest(TestCase):

    def setUp(self):
        self.pathiter = KINDLE_BOOKS

    def test_mobi_funcs(self):
        for path in self.pathiter:
            self.assertIn(path.suffix,[".azw3",".azw",".kfx"])
            meta = KindleMeta(path)
            self.assertTrue(KindleMeta)
            self.assertEqual(meta.suffix,path.suffix)
            self.assertEqual(meta.stem,path.stem)
            self.assertEqual(meta.name,path.name)
            self.assertEqual(meta.data,path.read_bytes())
            self.assertTrue(meta.metadata)
            print(meta.palmheader)
            print(meta.palmname)
            print(meta.metadata)

    def test_metadata(self):
        for path in self.pathiter:
            path = abspath(path)
            meta = KindleMeta(path)
            self.assertTrue(meta.path.exists())
            metadata = meta.get_metadata()
            self.assertIn("filename",metadata)
            self.assertIn("extension",metadata)
            self.assertIn("size",metadata)
            self.assertIn("path",metadata)
