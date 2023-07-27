# ebookatty

![License](https://img.shields.io/badge/License-LGPL-blue?style=for-the-badge&logo=appveyor)
![Testing](https://img.shields.io/badge/Testing-Pytest-orange?style=for-the-badge&logo=appveyor)
![Python](https://img.shields.io/badge/Python-3.0%2B-red?style=for-the-badge&logo=appveyor)

-------------------------

Simple utility that extracts embedded metadata in common ebook formats. Works on mobi epub and most amazon kindle filetypes.
Works as a CLI or can be used as a library. Usage details and examples provided below.

## Features

* Successfully extracts metadata from .mobi .kfx .epub .azw .azw3 file formats
* No external dependencies
* Displays every bit of metadata information it finds and leaves out blh

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
from ebookatty import MetadataFetcher
```

## License / EULA

GNU LGPL v3.0
[LICENSE FILE](./LICENSE.md)


## Usage

### Example Use

__example 1__
```bash
ebookatty /path/to/ebooks/*.epub
```

__example 2__
```
ebookatty **/**/*.mobi
```

__example 3__
```
ebookatty /path/to/specific/ebook.azw3
```


__example output__
```
---------------------------------------------------------------------------------------------------------------------------------------------
Title           A Philosophy of Software Design
Publisher       Yaknyam Press, Palo Alto, CA
Creator         John Ousterhout
Language        en
Contributor     calibre (3.33.1) [https://calibre-ebook.com]
Date            2019-01-22T08:00:00+00:00
Rights          Copyright 2018 John K. Ousterhout
Subject         modular decomposition; interface vs. implementation; computer programming; abstraction; software design; software complexity
Identifier      B07N1XLQ7D; urn:uuid:19682118-2a9c-49ed-b1e9-1ceb58110b6f
---------------------------------------------------------------------------------------------------------------------------------------------

--------------------------------------------------------------------
Author          Friedrich Wilhelm Nietzsche
Title           Beyond Good and Evil
Rights          Public domain in the USA.
Tags            Philosophy; Ethics; German
Pubdate         2003-08-01T04:00:00+00:00
Book_Producer   calibre (4.17.0) [http://calibre-ebook.com]
Uuid            3f455008-90c8-40e8-8366-69b599b36a9a
Codec           utf-8
Doctype         MOBI; EXTH
Unique_Id       1417459778
Identity        BOOKMOBI
Type            2
Version         6
Name            Beyond Good and Evil by Friedrich Wilhelm Nietzsche
--------------------------------------------------------------------

--------------------------------------------------------------
Title           The First Six Books of the Elements of Euclid
Creator         John Casey; Euclid
Language        en
Date            2022-08-10T09:11:00.913013+00:00; 2007-04-14
Rights          Public domain in the USA.
Subject         Mathematics, Greek; Euclid's Elements
Identifier      http://www.gutenberg.org/21076
--------------------------------------------------------------

----------------------------------------------------------------------------------------------------------------------------------------------------------
Author          William Shakespeare
Title           Romeo and Juliet
Publisher       HarperCollins
Rights          NONE
Isbn            9780061965494
Pubdate         2009-08-15T07:00:00+00:00
Book_Producer   calibre (0.7.23) [http://calibre-ebook.com]
Codec           utf-8
Doctype         MOBI; EXTH
Unique_Id       1974853891
Identity        BOOKMOBI
Type            2
Version         6
Name            Romeo and Juliet - William Shakespeare
Tags            Renaissance; Shakespeare plays; Love & Romance; Classics; Welsh; Historical; Man-woman relationships; 1564-1616; Shakespeare;
                Children's Books - Young Adult Fiction; Juliet (Fictitious character); Verona (Italy); Playscripts (Children's; Historical -
                Renaissance; YA); Conflict of generations; English; Young Adult Graphic Novels; Drama; General; Children: Young Adult (Gr. 7-9);
                Scottish; Juvenile Fiction; Irish; William; Children's Books; Romeo (Fictitious character); Vendetta; Young Adult General Interest &
                Leisure; Juvenile Nonfiction
Comments        SUMMARY: These violent delights have violent ends And in their triumph die, like fire and powder, Which, as they kiss, consume. When
                Romeo first lays eyes on the bewitching Juliet, it's love at first sight. But though their love runs true and deep, it is also completely
                forbidden. With family and fate determined to keep them apart, will Romeo and Juliet find a way to be together? William Shakespeare's
                masterpiece is one of the most enduring stories of star-crossed love of all time. Beautifully presented for a modern teen audience with
                both the original play and a prose retelling of the beloved story, this is the must-have edition of a timeless classic.
----------------------------------------------------------------------------------------------------------------------------------------------------------

-------------------------------------------------------------------------------------------------------------------------------------------------
Author          Margaret Mitchell
Title           Gone with the wind
Publisher       Avon Books
Tags            Unread; Fiction
Comments        SUMMARY:  The turbulent romance of Scarlett O'Hara and Rhett Butler is shaped by the ravages of the Civil War and Reconstruction
Isbn            9780380001095
Pubdate         1973-10-14T22:00:00+00:00
Book_Producer   calibre (0.8.46) [http://calibre-ebook.com]
Codec           utf-8
Doctype         MOBI; EXTH
Unique_Id       2030054980
Identity        BOOKMOBI
Type            2
Version         6
-------------------------------------------------------------------------------------------------------------------------------------------------

-----------------------------------------------------------------------------------------------------------------------------------------------
Author          Plato
Title           The Republic
Rights          Public domain in the USA.
Tags            Utopias -- Early works to 1800; Justice -- Early works to 1800; Classical literature; Political science -- Early works to 1800
Pubdate         1998-10-01T04:00:00+00:00
Book_Producer   calibre (4.17.0) [http://calibre-ebook.com]
Uuid            7422f1b5-a40a-4579-8945-def5c386c88e
Codec           utf-8
Doctype         MOBI; EXTH
Unique_Id       2377915433
Identity        BOOKMOBI
Type            2
Version         6
Name            The Republic - Plato
-----------------------------------------------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------------------------
Author          Unknown
Title           The Jargon File, Version 2.9.10, 01 Jul 1992
Rights          Public domain in the USA.
Tags            Computers -- Slang -- Dictionaries; Electronic data processing -- Terminology -- Humor; Computers -- Humor
Pubdate         1992-08-01T00:00:00+00:00
Book_Producer   calibre (3.14.0) [https://calibre-ebook.com]
Uuid            fbd99707-2c14-44b9-99c3-09d444860816
Codec           utf-8
Doctype         MOBI; EXTH
Unique_Id       2480398827
Identity        BOOKMOBI
Type            2
Version         8
Name            The-Hacker's-Dictionary
---------------------------------------------------------------------------------------------------------------------------

-----------------------------------------------------
Title           The Kama Sutra of Vatsayayana
Creator         Unknown
Language        en
Identifier      80e2d8c5-6ced-4337-9300-92ab5bd9d311
-----------------------------------------------------

------------------------------------------------------------
Title           The New Hacker"s Dictionary
Pubdate         2017-12-25T18:05:35.914130+00:00
Book_Producer   calibre (3.14.0) [http://calibre-ebook.com]
Uuid            2ea796bd-f62a-48b8-be48-83ae9606f757
Codec           utf-8
Doctype         MOBI; EXTH
Unique_Id       2418361619
Identity        BOOKMOBI
Type            2
Version         8
Name            The-New-Hacker's-Dictionary
------------------------------------------------------------
```
