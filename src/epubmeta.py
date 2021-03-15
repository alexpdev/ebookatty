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
        self.types = {
            1	:"drm_server_id",#
            2	:"drm_commerce_id",#
            3	:"drm_ebookbase_book_id",#
            100	:"author",#		<dc:Creator>
            101	:"publisher",#		<dc:Publisher>
            102	:"imprint",#		<Imprint>
            103	:"description",#		<dc:Description>
            104	:"isbn",#		<dc:Identifier scheme='ISBN'>
            105	:"subject",#	Could appear multiple times	<dc:Subject>
            106	:"publishingdate",#		<dc:Date>
            107	:"review",#		<Review>
            108	:"contributor",#		<dc:Contributor>
            109	:"rights",#		<dc:Rights>
            110	:"subjectcode",#		<dc:Subject BASICCode="subjectcode">
            111	:"type",#		<dc:Type>
            112	:"source",#		<dc:Source>
            113	:"asin",#	Kindle Paperwhite labels books with "Personal" if they don't have this record.
            114	:"versionnumber",#
            115	:"sample",#	0x0001 if the book content is only a sample of the full book
            116	:"startreading",#	Position (4-byte offset) in file at which to open when first opened
            117	:"adult",#	Mobipocket Creator adds this if Adult only is checked on its GUI; contents: "yes"	<Adult>
            118	:"retail",# price	As text, e.g. "4.99"	<SRP>
            119	:"retail",# price currency	As text, e.g. "USD"	<SRP Currency="currency">
            121	:"KF8",# BOUNDARY Offset
            125	:"count",# of resources
            129	:"KF8",# cover URI
            131	:"Unknown",#
            200	:"Dictionary",# short name	As text	<DictionaryVeryShortName>
            201	:"coveroffset",#	Add to first image field in Mobi Header to find PDB record containing the cover image	<EmbeddedCover>
            202	:"thumboffset",#	Add to first image field in Mobi Header to find PDB record containing the thumbnail cover image
            203	:"hasfakecover",#
            204	:"Creator",# Software	Known Values: 1=mobigen, 2=Mobipocket Creator, 200=kindlegen (Windows), 201=kindlegen (Linux), 202=kindlegen (Mac).
            205	:"Creator",# Major Version
            206	:"Creator",# Minor Version
            207	:"Creator",# Build Number
            208	:"watermark",#
            209	:"tamper",# proof keys	Used by the Kindle (and Android app) for generating book-specific PIDs.
            300	:"fontsignature",#
            401	:"clippinglimit",#	Integer percentage of the text allowed to be clipped. Usually 10.
            402	:"publisherlimit",#
            403	:"Unknown",#
            404	:"ttsflag",#	1 - Text to Speech disabled; 0 - Text to Speech enabled
            405	:"Unknown",# (Rent/Borrow flag?)	1 in this field seems to indicate a rental book
            406	:"Rent",#/Borrow Expiration Date	If this field is removed from a rental, the book says it expired in 1969
            407	:"Unknown",#
            450	:"Unknown",#
            451	:"Unknown",#
            452	:"Unknown",#
            453	:"Unknown",#
            501	:"cdetype",#	PDOC - Personal Doc; EBOK - ebook; EBSP - ebook sample;
            502	:"lastupdatetime",#
            503	:"updatedtitle",#
            504	:"asin",#	I found a copy of ASIN in this record.
            524	:"language",#		<dc:language>
            525	:"writingmode",#	I found horizontal-lr in this record.
            535	:"Creator",# Build Number	I found 1019-d6e4792 in this record, which is a build number of Kindlegen 2.7
            536	:"Unknown",#
            542	:"Unknown",#	Some Unix timestamp.
            547	:"InMemory",#	String 'I\x00n\x00M\x00e\x00m\x00o\x00r\x00y\x00' found in this record, for KindleGen V2.9 build 1029-0897292
        }
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
