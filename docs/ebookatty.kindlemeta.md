<!-- markdownlint-disable -->

<a href="..\ebookatty\kindlemeta.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `ebookatty.kindlemeta`
Module contains implementation specific to amazon formatted ebooks. 

Classes and functions for .azw, .azw3, and .kfx ebooks. 

**Global Variables**
---------------
- **EXTH_Types**


---

<a href="..\ebookatty\kindlemeta.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `KindleMeta`
Gather Epub Metadata. 

<a href="..\ebookatty\kindlemeta.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `KindleMeta.__init__`

```python
__init__(path)
```

Construct the EpubMeta Class Instance. 



**Args:**
 
 - <b>`path`</b> (str or pathlike):  path to ebook file. 




---

<a href="..\ebookatty\kindlemeta.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `KindleMeta.find_metadata`

```python
find_metadata()
```

Find the offset to the EXTH header. 

---

<a href="..\ebookatty\kindlemeta.py#L99"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `KindleMeta.get_metadata`

```python
get_metadata()
```

Extract metadata from ebook. 



**Returns:**
 
 - <b>`dict`</b>:  key, value pairs of metadata. 

---

<a href="..\ebookatty\kindlemeta.py#L67"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `KindleMeta.unLongx`

```python
unLongx(total, x)
```

Convert bits to text. 



**Args:**
 
 - <b>`total`</b> (int):  number of bytes to decode 
 - <b>`x`</b> (bytes):  bytes to decode 



**Returns:**
 
 - <b>`str`</b>:  decoded bytes 

---

<a href="..\ebookatty\kindlemeta.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `KindleMeta.unShort`

```python
unShort(x)
```

Convert bits to text. 



**Args:**
 
 - <b>`x`</b> (bytes):  bytes to decode 



**Returns:**
 
 - <b>`str`</b>:  decoded bytes 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
