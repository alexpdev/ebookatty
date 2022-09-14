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
"""Utility functions and methods."""

from glob import glob
from pathlib import Path
import json
import sys
import argparse
import csv

from ebookatty import get_metadata

def find_matches(files):
    """Find files that match the patterns."""
    matches = []
    for file in files:
        matches += glob(file)
    return matches


def execute():
    parser = argparse.ArgumentParser(description="get ebook metadata", prefix_chars="-")
    parser.add_argument('file', help='path to ebook file(s), standard file pattern extensions are allowed.', nargs=1)
    parser.add_argument('-o', '--output', help='file path where metadata will be written. Acceptable formats include json and csv and are determined based on the file extension. Default is None', action="store")
    if len(sys.argv[1:]) == 0:
        sys.argv.append("-h")
    args = parser.parse_args(sys.argv[1:])
    file_list = args.file
    matches = find_matches(file_list)
    datas = []
    for match in matches:
        data = get_metadata(match)
        datas.append(data)
    if args.output:
        path = Path(args.output)
        if path.suffix == ".json":
            json.dump(datas, open(path,"wt"))
        elif path.suffix == ".csv":
            d = set()
            for row in datas:
                for key in row.keys():
                    d.add(key)
            headers = list(d)
            layers = [headers]
            for row in datas:
                layer = []
                for header in headers:
                    record = row.get(header, "")
                    if isinstance(record, list):
                        record = record[0]
                    if isinstance(record, int):
                        record = str(record)
                    if isinstance(record, bytes):  # pragma: nocover
                        record = str(record[0], encoding="utf8", errors="ignore")
                    layer.append(record)
                layers.append(layer)
            print(layers)
            with open(path, "wt", encoding="utf-8", errors="ignore") as fd:
                for layer in layers:
                    fd.write(",".join(layer) + "\n")
