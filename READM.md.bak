# pybook_metadata

Version 0.1.1

## License / EULA

GNU LGPL v3.0
[LICENSE FILE](./LICENSE)

## Overview

- Simple tool for extracting metadata fields from the more popular ebook formats.
- Can be used as a CLI or a Library
- Tested on the most common ebook filestypes _e.g._ epub, mobi, azw3, azw, kfx...
- 100% Pure Python from the standard library
- No external dependencies
- Tested working for Python 3+
- full suite of unittests for each component

## Requirements

- Python 3+
- Tested on Windows and Linux

## Instructions

Using as a command line interface is super easy:

- `cd "Project Directory"`
- `python3 pybook_metadata.py [-f/--file "ebook.mobi"] [-d ["ebookfolder/"]]`

For use as a library

- `from pybook_metadata import get_metadata, MetadataFetcher`

The get_metadata(path) function that takes one arguement, ebook filepath or path-like. The function returns a dictionary of `{"field" : value}` pairs.

The MetadataFetcher class has one primary method `metadatafetcher.get_metadata()`, which stores the information in the `.metadata` attribute.

Unless improperly formatted every file is guaranteed to include Title, Creator, Publisher, Description, and Identifier. Also included is the filename, path, filesize, and extension format, plus whatever other metadata is included in the file.

[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)

## TODO

- Include cover art location as a field
- Include optional table of contents as field
- I may decide to expand it to allow editing the metadata as well
