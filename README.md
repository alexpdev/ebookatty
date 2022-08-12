# ebookatty

![License](https://img.shields.io/badge/License-LGPL-blue?style=for-the-badge&logo=appveyor)
![Testing](https://img.shields.io/badge/Testing-Pytest-orange?style=for-the-badge&logo=appveyor)
![Python](https://img.shields.io/badge/Python-3.0%2B-red?style=for-the-badge&logo=appveyor)

-------------------------

Simple utility that extracts embedded metadata in common ebook formats. Works on mobi epub and most amazon kindle filetypes.
Includes a library of classes and functions for dealing with metadata, as well as a CLI to use as a standalone tool.
It is still a work in progress.

## Features

* succesfully extracts metadata from .mobi .kfx .epub .azw .azw3 file formats
* Extremely simple
* requires no external dependencies

## Requirements

* Python 3.3+
* Tested on Windows and Linux

## Installing

```Linux
pip install ebookatty
```

## Instructions

Using as a command line interface is super easy:

```Linux
ebookatty path/to/ebook.epub
```

or import into your project...

```python
from ebookatty import get_metadata, MetadataFetcher
```

## License / EULA

GNU LGPL v3.0
[LICENSE FILE](./LICENSE.md)


## Usage

### Example Use

```bash
ebookatty /path/to/ebooks/*.epub
```

> stdout
```txt
---------------------------------------------------------------------------------------------
Filename        A Connecticut Yankee in King Arthur's Court - Mark Twain.epub
Path            /path/to/ebooks/A Connecticut Yankee in King Arthur's Court - Mark Twain.epub
Extension       .epub
Size            29765765
Title           Connecticut Yankee in King Arthur's Court (Barnes & Noble Classics Series)
Publisher       Barnes & Noble
Creator         Mark Twain
Language        en
Date            NONE
---------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------
Filename        A Philosophy of Software Design - John Ousterhout.epub
Path            /path/to/ebooks/A Philosophy of Software Design - John Ousterhout.epub
Extension       .epub
Size            720696
Title           A Philosophy of Software Design
Publisher       Yaknyam Press, Palo Alto, CA
Creator         John Ousterhout
Language        en
Contributor     calibre (3.33.1) [https://calibre-ebook.com]
Date            2019-01-22T08:00:00+00:00
------------------------------------------------------------------------------------

--------------------------------------------------------------------------------------------------------
Filename        Elements of Euclid - John Casey and Euclid.epub
Path            /path/to/ebooks/Elements of Euclid - John Casey and Euclid.epub
Extension       .epub
Size            1344988
Title           The First Six Books of the Elements of Euclid
Creator         John Casey, Euclid
Language        en
Date            2007-04-14 2022-08-10T09:11:00.913013+00:00
--------------------------------------------------------------------------------------------------------
```

```bash
ebookatty **/**/*.mobi
```

```txt
--------------------------------------------------------------------------------------
Filename        Beyond Good and Evil by Friedrich Wilhelm Nietzsche.mobi
Path            tests\testbooks\Beyond Good and Evil by Friedrich Wilhelm Nietzsche.mobi
Extension       .mobi
Size            355797
Author          Friedrich Wilhelm Nietzsche
Language        en
--------------------------------------------------------------------------------------

-------------------------------------------------------------------------
Filename        Romeo and Juliet - William Shakespeare.mobi
Path            tests\testbooks\Romeo and Juliet - William Shakespeare.mobi
Extension       .mobi
Size            883395
Author          William Shakespeare
Publisher       HarperCollins
-------------------------------------------------------------------------

---------------------------------------------------------
Filename        The Republic - Plato.mobi
Path            tests\testbooks\The Republic - Plato.mobi
Extension       .mobi
Size            807415
Author          Plato
Language        en
---------------------------------------------------------
```
