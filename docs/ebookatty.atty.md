<!-- markdownlint-disable -->

<a href="..\ebookatty\atty.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `ebookatty.atty`
Metadata Parsing and extracting from ebook files. 

ebookatty module. 


---

<a href="..\ebookatty\atty.py#L103"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_metadata`

```python
get_metadata(path)
```

Extract metadata from ebooks. 



**Args:**
 
 - <b>`path`</b> (str or path-like):  Path to ebook file. 



**Returns:**
 
 - <b>`dict`</b>:  Metadata keys and values embedded in the file. 


---

<a href="..\ebookatty\atty.py#L117"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `format_output`

```python
format_output(book)
```

Format the output for printing to STDOUT. 



**Args:**
 
 - <b>`book`</b> (str or path-like):  Path to ebook file 



**Returns:**
 
 - <b>`str`</b>:  Text data to output to STDOUT 


---

<a href="..\ebookatty\atty.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PathDoesNotExistError`
Raise when ebook path does not exist. 



**Args:**
 
 - <b>`Exception`</b> (Obj):  Raises an Exception 





---

<a href="..\ebookatty\atty.py#L45"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `UnsupportedFormatError`
Raise when ebook file format is unsupported. 



**Args:**
 
 - <b>`Exception`</b> (Obj):  Raises an Exception 





---

<a href="..\ebookatty\atty.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MetadataFetcher`
Primary Entrypoint for extracting metadata from most ebook filetypes. 

<a href="..\ebookatty\atty.py#L58"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `MetadataFetcher.__init__`

```python
__init__(path)
```

Construct the MetadataFetcher Class and return Instance. 



**Args:**
 
 - <b>`path`</b> (str or path-like):  The path to the ebook to extract from 



**Raises:**
 
 - <b>`UnsupportedFormatError`</b>:  When unknown format is encountered 




---

<a href="..\ebookatty\atty.py#L87"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `MetadataFetcher.get`

```python
get(path)
```

Get metadata from ebook at specified path. 



**Args:**
 
 - <b>`path`</b> (str or path-like):  Path to ebook. 



**Returns:**
 
 - <b>`dict`</b>:  Metadata keys and values embedded in the file. 

---

<a href="..\ebookatty\atty.py#L78"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `MetadataFetcher.get_metadata`

```python
get_metadata()
```

Call to start the extraction process. 



**Returns:**
 
 - <b>`dict`</b>:  Metadata keys and values embedded in the file. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
