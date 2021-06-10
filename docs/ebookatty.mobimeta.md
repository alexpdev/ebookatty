<!-- markdownlint-disable -->

<a href="..\ebookatty\mobimeta.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `ebookatty.mobimeta`
Module contains implementation specific to mobi formatted ebooks. 

Classes and functions for .mobi ebooks. 

**Global Variables**
---------------
- **EXTH_Types**


---

<a href="..\ebookatty\mobimeta.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MobiMeta`
Extract Metadata from mobi ebook. 

<a href="..\ebookatty\mobimeta.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `MobiMeta.__init__`

```python
__init__(path)
```

Construct the EpubMeta Class Instance. 



**Args:**
 
 - <b>`path`</b> (str or pathlike):  path to ebook file. 




---

<a href="..\ebookatty\mobimeta.py#L91"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `MobiMeta.find_metadata`

```python
find_metadata()
```

Find the offset to the EXTH header. 

---

<a href="..\ebookatty\mobimeta.py#L107"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `MobiMeta.get_metadata`

```python
get_metadata()
```

Extract metadata from ebook. 



**Returns:**
 
 - <b>`dict`</b>:  key, value pairs of metadata. 

---

<a href="..\ebookatty\mobimeta.py#L75"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `MobiMeta.unLongx`

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

<a href="..\ebookatty\mobimeta.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `MobiMeta.unShort`

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
