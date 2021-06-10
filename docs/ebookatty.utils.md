<!-- markdownlint-disable -->

<a href="..\ebookatty\utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `ebookatty.utils`
Parsing Utilities. 


---

<a href="..\ebookatty\utils.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `path_meta`

```python
path_meta(path)
```

Metadata extracted from the file and path names. 



**Args:**
 
 - <b>`path`</b> (str):  path to file 



**Returns:**
 
 - <b>`dict`</b>:  key, value pairs of metadata parsed. 


---

<a href="..\ebookatty\utils.py#L57"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `reverse_tag_iter`

```python
reverse_tag_iter(block)
```

Decode tag names. 



**Args:**
 
 - <b>`block`</b> (bytes):  tag names 



**Yields:**
 
 - <b>`str`</b>:  tag name 


---

<a href="..\ebookatty\utils.py#L79"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `getLanguage`

```python
getLanguage(langID, sublangID)
```

Get Language Standard. 



**Args:**
 
 - <b>`langID`</b> (str):  Landguage ID 
 - <b>`sublangID`</b> (str):  Sublanguage ID 



**Returns:**
 
 - <b>`str`</b>:  Language encoding. 


---

<a href="..\ebookatty\utils.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `HeaderMissingError`
Raise HeaderMissingError. 





---

<a href="..\ebookatty\utils.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MetadataError`
Raise MetadataError. 







---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
