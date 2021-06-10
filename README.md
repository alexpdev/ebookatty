# ebookatty

![License](https://img.shields.io/badge/License-LGPL-blue?style=for-the-badge&logo=appveyor)
![Testing](https://img.shields.io/badge/Testing-Pytest-orange?style=for-the-badge&logo=appveyor)
![Python](https://img.shields.io/badge/Python-3.0%2B-red?style=for-the-badge&logo=appveyor)

-------------------------

Simple utility that extracts embedded metadata in common ebook formats. Works on mobi epub and most amazon kindle filetypes.
Includes a library of classes and functions for dealing with metadata, as well as a CLI to use as a standalone tool.

## Requirements

* Python 3.3+
* pip
* Tested on Windows and Linux
* pytest for unittesting source

## Installing

```Linux
pip install ebookatty-alexpdev
```

## Instructions

Using as a command line interface is super easy:

```Linux
ebookatty -d path/to/ebooks.mobie
```

or import into your project...

```python
from ebookatty import get_metadata, MetadataFetcher
```

[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)

## License / EULA

GNU LGPL v3.0
[LICENSE FILE](./LICENSE.md)

## ChangeLog

> version 0.1 core source code.
> version 0.2 capable of importing as external library

## TODO

* Work on CLI
* Include cover art location as a field
* Include optional table of contents as field
* I may decide to expand it to allow editing the metadata as well
