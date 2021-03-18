#! /usr/bin/python3
# -*- coding: utf-8 -*-

import re
import zipfile
from xml.etree import ElementTree as ET
from pathlib import Path
from src.utils import MetadataError, path_meta
from src.standards import _OPF_PARENT_TAGS


class EpubMeta:

    def __init__(self,path):
        self.tags = [
            "dc:title",
            "dc:contributor",
            "dc:creator",
            "dc:identifier",
            "dc:language",
            "dc:publisher",
            "dc:date",
            "dc:description",
            "dc:subject",
            "dc:rights",
            "creator",
            "publisher",
            "title",
            "language",
            "description",
            "subject"
        ]
        self.path = Path(path)
        self.name = self.path.name
        self.stem = self.path.stem
        self.suffix = self.path.suffix
        self.zipfile = zipfile.ZipFile(self.path)
        self.metadata = []
        self.find_metadata()

    def __str__(self):
        return f"EpubMeta({str(self.path)})"

    def get_opf(self):
        for fname in self.zipfile.namelist():
            if fname.endswith(".opf"):
                return fname
        raise Exception

    def find_metadata(self):
        with self.zipfile as zfile:
            opf_file = self.get_opf()
            with zfile.open(opf_file,"r") as zfile:
                ztext = zfile.read()
                self.xpath_parse(ztext)
                self.pattern_parse(ztext)
        return self.metadata

    def pattern_parse(self,opf):
        text = str(opf)
        metadata = []
        for tag in self.tags:
            pat1 = re.compile(f"<{tag}.*?>(.*)</{tag}",re.S | re.M)
            result = pat1.search(text)
            if result:
                groups = result.groups()
                if isinstance(groups,str):
                    record = (tag,groups)
                    metadata.append(record)
                else:
                    for group in groups:
                        record = (tag,group)
                        metadata.append(record)
        self.metadata += metadata

    def xpath_parse(self,opf):
        root = ET.fromstring(opf)
        ns = {
            "dc" : "http://purl.org/dc/elements/1.1/",
            "opf" : "http://www.idpf.org/2007/opf",
            "xsi":"http://www.w3.org/2001/XMLSchema-instance",
            "dcterms":"http://purl.org/dc/terms/",
        }
        metadata = []
        for tag in self.tags:
            matches = root.findall(tag,ns)
            records = [(tag,match.text) for match in matches]
            metadata += records
        self.metadata += metadata

    def get_metadata(self):
        self.metadata += path_meta(self.path)
        meta = {}
        for k,v in self.metadata:
            if "dc:" in k:
                k = k[3:]
            if k in meta:
                meta[k].append(v)
            else:
                meta[k] = [v]
        return meta
