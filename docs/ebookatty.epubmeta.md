<!-- markdownlint-disable -->

<a href="..\ebookatty\epubmeta.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `ebookatty.epubmeta`
Contains implementation specific to epub formatted ebooks. 

Classes and functions for .epub files. 



---

<a href="..\ebookatty\epubmeta.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `EpubMeta`
Gather Epub Metadata. 

<a href="..\ebookatty\epubmeta.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `EpubMeta.__init__`

```python
__init__(path)
```

Construct the EpubMeta Class Instance. 



**Args:**
 
 - <b>`path`</b> (str or pathlike):  path to ebook file. 




---

<a href="..\ebookatty\epubmeta.py#L95"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `EpubMeta.find_metadata`

```python
find_metadata()
```

Find metadata within the ebook archive file. 



**Returns:**
 
 - <b>`dict`</b>:  key,value pairs for ebook metadata 

---

<a href="..\ebookatty\epubmeta.py#L154"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `EpubMeta.get_metadata`

```python
get_metadata()
```

Extract and format metadata into a dictionary. 



**Returns:**
 
 - <b>`dict`</b>:  key,value pairs of metadata extracted. 

---

<a href="..\ebookatty\epubmeta.py#L80"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `EpubMeta.get_opf`

```python
get_opf()
```

Get the .opf file within the ebook archive. 



**Raises:**
 
 - <b>`MetadataError`</b>:  If it cannot parse metadata file 



**Returns:**
 
 - <b>`(str)`</b>:  the path to the .opf file. 

---

<a href="..\ebookatty\epubmeta.py#L110"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `EpubMeta.pattern_parse`

```python
pattern_parse(opf)
```

Parse .opf file for Metadata using regex. and xpath. 



**Args:**
 
 - <b>`opf`</b> (str):   path to opf file 

---

<a href="..\ebookatty\epubmeta.py#L133"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `EpubMeta.xpath_parse`

```python
xpath_parse(opf)
```

Parse .opf file with xpath selectors. 



**Args:**
 
 - <b>`opf`</b> (str):  path to opf file to parse 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
