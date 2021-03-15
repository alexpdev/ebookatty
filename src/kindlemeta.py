import struct
from pathlib import Path
from src.utils import MetadataError, HeaderMissingError, BaseMeta

class KindleMeta(BaseMeta):

    def __init__(self,path):
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
        self.path = Path(path)
        self.name = self.path.name
        self.stem = self.path.stem
        self.suffix = self.path.suffix
        self.data = self.path.read_bytes()
        self.palmheader = self.data[:78]
        self.palmname = self.data[:32]
        self.metadata = []
        self.find_metadata()

    def unShort(self,x):
        buffer = self.data
        val = struct.unpack_from(">H", buffer, x)
        return val

    def unLongx(self,total,x):
        buffer = self.data
        form = ">" + ("L"*total)
        val = struct.unpack_from(form, buffer, x)
        return val

    def find_metadata(self):
        """ Find the offset to the EXTH header """
        super().find_metadata()
        offset = self.data.find(b'EXTH')
        if offset < 0:
            raise HeaderMissingError(self.path)
        _,headLen,recCount = self.unLongx(3,offset)
        print(headLen)
        offset += 12
        for _ in range(recCount):
            id, size = self.unLongx(2,offset)
            content = self.data[offset + 8 : offset + size]
            record = (id , content)
            self.metadata.append(record)
            offset += size
        if len(self.metadata) < 1:
            raise MetadataError(self.path)

    def get_metadata(self):
        meta = {}
        for k,v in self.metadata:
            if hasattr(v,"decode"):
                v = v.decode(errors="replace")
            if k in self.types:
                type_ = self.types[k]
                if type_ not in meta:
                    meta[type_] = [v]
                else:
                    meta[type_].append(v)
            else:
                if str(k) not in meta:
                    meta[str(k)] = [v]
                else:
                    meta[str(k)].append(v)
        return meta
