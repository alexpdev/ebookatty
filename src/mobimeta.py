import sys,os
import struct
from pathlib import Path
from os.path import abspath,dirname
sys.path(dirname(dirname(abspath(__file__))))
from data.paths import MOBI_PATH




class MobiMeta:

    def __init__(self,path):
        self.path = path
        self.name = path.name
        self.stem = path.stem
        self.suffix = path.suffix
        self.data = path.read_bytes()
        self.meta = {}

    def set_meta(self,field,value):
        pass

    def unLong(self,x):
        return lambda x: struct.unpack_from(">L", self.data, x)
    
    def unShort(self,x):
        return lambda x: struct.unpack_from(">H", self.data, x)

    def parse_meta(self):
        exth = self.data.find(b'EXTH')
        self.eHeader = {}



if __name__ == '__main__':
    mobis = MOBI_PATH.iterdir()
    book = MobiMeta(next(mobis))

