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
from typing import List, Optional, TextIO

from ebookatty.metadata import MetadataFetcher, format_output


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


def _determine_format(selected_format: Optional[str], output_target: Optional[str]) -> str:
    """Resolve the format that should be used for emitting metadata."""
    if selected_format:
        return selected_format
    if output_target and output_target != "-":
        suffix = Path(output_target).suffix.lower()
        if suffix == ".json":
            return "json"
        if suffix == ".csv":
            return "csv"
    return "table"


def _normalize_csv_value(record):
    if isinstance(record, list):
        record = record[0]
    if isinstance(record, int):
        record = str(record)
    if isinstance(record, bytes):  # pragma: nocover
        try:
            record = str(record[0], encoding="utf8", errors="ignore")
        except Exception:  # pragma: nocover
            return ""
    return record if isinstance(record, str) else str(record or "")


def _write_csv(datas, stream: TextIO) -> None:
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
            record = _normalize_csv_value(record)
            layer.append(record)
        layers.append(layer)
    for layer in layers:
        try:
            stream.write(",".join(layer) + "\n")
        except Exception:  # pragma: nocover
            continue


def _write_json(datas, stream: TextIO) -> None:
    json.dump(datas, stream)
    stream.write("\n")


def _write_table(datas, stream: TextIO) -> None:
    for row in datas:
        if not row:
            continue
        table = format_output(row, emit=False)
        stream.write(table)


def _emit_output(datas, output_format: str, output_target: Optional[str]) -> None:
    if output_target and output_target != "-":
        kwargs = {"encoding": "utf-8"}
        if output_format == "csv":
            kwargs["errors"] = "ignore"
        stream: TextIO = open(Path(output_target), "w", **kwargs)
        close_stream = True
    else:
        stream = sys.stdout
        close_stream = False
    try:
        if output_format == "json":
            _write_json(datas, stream)
        elif output_format == "csv":
            _write_csv(datas, stream)
        elif output_format == "table":
            _write_table(datas, stream)
    finally:
        if close_stream:
            stream.close()


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
        help="file path where metadata will be written. Use '-' to send data to STDOUT. Acceptable formats include json and csv and are determined based on the file extension. Default is None",
        action="store",
    )
    parser.add_argument(
        "-F",
        "--format",
        choices=["table", "json", "csv"],
        help="output format to use for metadata. Defaults to 'table' (plain text) unless an output file extension specifies json or csv.",
        dest="output_format",
    )
    if len(sys.argv[1:]) == 0:
        sys.argv.append("-h")
    args = parser.parse_args(sys.argv[1:])
    file_list = args.file
    matches = find_matches(file_list)
    datas = []
    output_format = _determine_format(args.output_format, args.output)
    show_table_now = output_format == "table" and not args.output
    for match in matches:
        fetcher = MetadataFetcher(match)
        data = fetcher.get_metadata()
        datas.append(data)
        if show_table_now:
            fetcher.show_metadata()
    needs_output = bool(args.output) or output_format in ("json", "csv")
    if needs_output:
        _emit_output(datas, output_format, args.output)
