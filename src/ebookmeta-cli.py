#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from os.path import dirname,abspath
from argparse import ArgumentParser
sys.path.append(dirname(dirname(abspath(__file__))))
from src.ebook_metadata import get_metadata

def format_output(meta,path):
    output = path + "\n" + ("-"*len(path)) + "\n"
    maxlen = max([len(i) for i in meta.keys()]) * 2
    diff = 90 - maxlen
    for k,v in meta.items():
        line = k + (" "*(maxlen - len(k))) + "|"
        if len(v) > 1:
            v = ", ".join(v)
        else:
            v = str(v[0])
        vlen = len(v)
        if vlen > diff:
            vdiff = vlen - (vlen - diff)
            line += v[:vdiff] + "\n"
            line += (" "*maxlen) + v[vdiff:] + "\n"
        else:
            line += v + "\n"
        output += line
    return output



def cliparse(args):
    parser = ArgumentParser(description="get ebook metadata")
    parser.add_argument("-f","--file",nargs="+",help="file path(s) for ebooks")
    parser.add_argument("-d","--directory",action='append',help="file path(s) for ebooks")
    paths = parser.parse_args(args)
    for p in paths.path[0]:
        if os.path.exists(p):
            metadata = get_metadata(p)
            output = format_output(metadata,p)
            print(output)

if __name__ == "__main__":
    cliparse(sys.argv[1:])




