import sys
from unittest import TestCase
from os.path import abspath,dirname
sys.path.append(dirname(dirname(abspath(__file__))))
from data.paths import MOBI_BOOKS
from src.mobimeta import MobiMeta

class MobiTest(TestCase):

    def setUp(self):
        self.pathiter = MOBI_BOOKS

    def test_mobi_funcs(self):
        for path in MOBI_BOOKS:
            self.assertEqual(path.suffix,".mobi")
            mobimeta = MobiMeta(path)
            self.assertTrue(MobiMeta)
            self.assertEqual(mobimeta.suffix,path.suffix)
            self.assertEqual(mobimeta.stem,path.stem)
            self.assertEqual(mobimeta.name,path.name)
            self.assertEqual(mobimeta.data,path.read_bytes())
            self.assertTrue(mobimeta.metadata)




