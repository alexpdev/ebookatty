#! /usr/bin/python3
# -*- coding: utf-8 -*-

import re
from zipfile import ZipFile
from xml.etree import ElementTree as ET
from pathlib import Path
from src.utils import MetadataError, path_meta
from src.standards import _OPF_PARENT_TAGS


class EpubMeta:

    def __init__(self,path):
        self.tags = [
            "metadata",
            "dc:title",
            "dc:contributor",
            "dc:identifier",
            "dc:language",
            "dc:publisher",
            "dc:date",
            "dc:description",
            "dc:subject",
            "dc:rights",
            "dc:format",
            "identifier",
            "creator",
            "publisher",
            "title",
            "author",
            "language",
            "description",
            "subject"
        ]
        
        self.metafiles = [
            "content.opf",
        ]
        self.path = Path(path)
        self.name = self.path.name
        self.stem = self.path.stem
        self.suffix = self.path.suffix
        self.zipfile = ZipFile(self.path)
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
        opf_file = self.get_opf()
        try:
            self.xpath_parse(opf_file)
        except Exception as e:
            self.pattern_parse(opf_file)
        return self.metadata

    def pattern_parse(self,opf):
        text = self.zipfile.open(opf).read()
        lines = text.split(b"\n")
        metadata = []
        for tag in self.tags:
            pat1 = re.compile(b"<tag.*?>")
            pat2 = re.compile(b"<tag.?>")
            pat3 = re.compile(b"</metadata>")
            for line in lines:
                if pat3.search(line): break
                otag, ctag = pat1.search(line), pat2.search(line)
                if not otag: continue
                text = line[otag.end():ctag.start()]
                record = (tag,text)
                metadata.append(record)
        self.metadata += metadata

    def xpath_parse(self,opf):
        et = ET(self.zipfile.open(opf))
        root = et.getroot()
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
        if not metadata:
            raise MetadataError
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
