import re
import json
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from ebookatty.standards import OPF_tags

class Epub:
    """Gather Epub Metadata."""

    def __init__(self, path):
        """
        Construct the EpubMeta Class Instance.

        Args:
            path (str or pathlike): path to ebook file.
        """
        self.tags = OPF_tags
        self.path = Path(path)
        self.epub_zip = zipfile.ZipFile(self.path)
        self.stem = self.path.stem
        self.suffix = self.path.suffix
        self.opf = self.get_opf()
        self.opf_data = self.epub_zip.read(self.opf).decode()
        root = ET.fromstring(self.opf_data)
        meta = self.iterer(root)
        for key, val in meta.items():
            if val:
                val = '; '.join([str(i) for i in set(val)])
                meta[key] = val
        self.metadata = meta

    def iterer(self, root):
        pattern = re.compile(r'\{.*\}(\w+)')
        match = pattern.findall(root.tag)[0]
        if match in self.tags:
            meta = {match: [root.text]}
        else:
            meta = {}
        for element in root:
            if element != root:
                data = self.iterer(element)
                for k,v in data.items():
                    meta.setdefault(k,[])
                    meta[k].extend(v)
        return meta

    def get_opf(self):
        ns = {'n': 'urn:oasis:names:tc:opendocument:xmlns:container',
              'pkg': 'http://www.idpf.org/2007/opf',
              'dc': 'http://purl.org/dc/elements/1.1/'}
        txt = self.epub_zip.read('META-INF/container.xml')
        tree = ET.fromstring(txt)
        elems = tree.findall('n:rootfiles/n:rootfile', namespaces=ns)
        for elem in elems:
            if 'full-path' in elem.attrib:
                return elem.attrib['full-path']
        return None
