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

import argparse
import json
import sys
from glob import glob
from pathlib import Path
from typing import List

from ebookatty import MetadataFetcher


def find_matches(files: List[str]) -> List[str]:
    """
    Search list and find matching file paths that fit patterns.

    Parameters
    ----------
    files : list
        list of files and patterns to seach for

    Returns
    -------
    list
        the full absolute or relative path to matching file
    """
    matches = []
    for file in files:
        matches += glob(file)
    return matches


def execute():
    """
    Execute the program.

    This is the applications main entrypoint and CLI implementation.
    """
    parser = argparse.ArgumentParser(description="get ebook metadata", prefix_chars="-")
    parser.add_argument(
        "file",
        help="path to ebook file(s), standard file pattern extensions are allowed.",
        nargs=1,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="file path where metadata will be written. Acceptable formats include json and csv and are determined based on the file extension. Default is None",
        action="store",
    )
    if len(sys.argv[1:]) == 0:
        sys.argv.append("-h")
    args = parser.parse_args(sys.argv[1:])
    file_list = args.file
    matches = find_matches(file_list)
    datas = []
    for match in matches:
        fetcher = MetadataFetcher(match)
        data = fetcher.get_metadata()
        datas.append(data)
        if not args.output:
            fetcher.show_metadata()
    if args.output:
        path = Path(args.output)
        if path.suffix == ".json":
            json.dump(datas, open(path, "wt"))
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
                        try:
                            record = str(record[0], encoding="utf8", errors="ignore")
                        except:
                            continue
                    layer.append(record)
                layers.append(layer)
            with open(path, "wt", encoding="utf-8", errors="ignore") as fd:
                for layer in layers:
                    try:
                        fd.write(",".join(layer) + "\n")
                    except:
                        continue
