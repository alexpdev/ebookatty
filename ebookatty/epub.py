import re
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET


def split_authors(values):
    authors_list = []
    for value in values:
        authors = re.split('[&;]', value)
        for author in authors:
            commas = author.count(',')
            if commas == 1:
                author_split = author.split(',')
                authors_list.append(author_split[1].strip() + ' ' + author_split[0].strip())
            elif commas > 1:
                authors_list.extend([x.strip() for x in author.split(',')])
            else:
                authors_list.append(author.strip())
    return authors_list


def get_sorted_author(value):
    value2 = None
    try:
        if ',' not in value:
            regexes = [r"^(JR|SR)\.?$", r"^I{1,3}\.?$", r"^IV\.?$"]
            combined = "(" + ")|(".join(regexes) + ")"
            value = value.split(" ")
            if re.match(combined, value[-1].upper()):
                if len(value) > 1:
                    value2 = value[-2] + ", " + " ".join(value[:-2]) + " " + value[-1]
                else:
                    value2 = value[0]
            elif len(value) == 1:
                value2 = value[0]
            else:
                value2 = value[-1] + ", " + " ".join(value[:-1])
        else:
            value2 = value
    except Exception:
        if isinstance(list, value2):
            value2 = value[0]
        else:
            value2 = value
    return value2

class Epub:
    """Gather Epub Metadata."""

    def __init__(self, path):
        """
        Construct the EpubMeta Class Instance.

        Args:
            path (str or pathlike): path to ebook file.
        """
        self.tags = ["dc:title", "dc:contributor", "dc:creator", "dc:identifier",
                     "dc:language", "dc:publisher", "dc:date", "dc:description",
                     "dc:subject", "dc:rights", "creator", "publisher",
                     "title", "language", "description", "subject", "date",
                     "pubdate", "identifier", "rights", "contributor"]
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

    def merge(self, data1, data2):
        meta = {}
        for dict_ in [data1, data2]:
            print(dict_)
            data = self.normalize_metadata(dict_)
            for k, v in data.items():
                meta.setdefault(k,[])
                meta[k].extend(v)
        return meta

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
