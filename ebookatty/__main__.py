#! /usr/bin/python3
# -*- coding: utf-8 -*-

########################################################################
#  Copyright (C) 2021  alexpdev
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#########################################################################
"""EbookData __main__ CLI interface."""


import sys
from argparse import ArgumentParser
from ebookatty import get_metadata

def main():
    parser = ArgumentParser(description="get ebook metadata")
    parser.add_argument('file', type=str, help='path to ebook file(s), standard file pattern extensions are allowed.', nargs="+")
    parser.add_argument('-r', '--recursive', help='recusively search for given file patterns')
    parser.add_argument('-o', '--output', help='file path where metadata will be written. Acceptable formats include json and csv and are determined based on the file extension. Default is None', action="store")
    args = parser.parse_args(sys.argv[1:])

    get_metadata(args.path)


if __name__ == "__main__":
    main()
