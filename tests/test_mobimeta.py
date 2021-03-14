import sys
from unittest import TestCase
from os.path import abspath,dirname
sys.path.append(dirname(dirname(abspath(__file__))))
from data.paths import TEST_PATH

class MobiTest(TestCase):

    def setUp(self):
        self.path = TEST_PATH

    def test_mobi_funcs(self):
        pass
