import re
import os
import zipfile
from xml.etree import ElementTree as etree


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

def get_epub_info(tmp_file_path, original_file_name, original_file_extension):
    ns = {
        'n': 'urn:oasis:names:tc:opendocument:xmlns:container',
        'pkg': 'http://www.idpf.org/2007/opf',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }

    epub_zip = zipfile.ZipFile(tmp_file_path)

    txt = epub_zip.read('META-INF/container.xml')
    tree = etree.fromstring(txt)
    cf_name = tree.xpath('n:rootfiles/n:rootfile/@full-path', namespaces=ns)[0]
    cf = epub_zip.read(cf_name)
    tree = etree.fromstring(cf)

    cover_path = os.path.dirname(cf_name)

    p = tree.xpath('/pkg:package/pkg:metadata', namespaces=ns)[0]

    epub_metadata = {}

    for s in ['title', 'description', 'creator', 'language', 'subject', 'publisher', 'date']:
        tmp = p.xpath('dc:%s/text()' % s, namespaces=ns)
        if len(tmp) > 0:
            if s == 'creator':
                epub_metadata[s] = ' & '.join(split_authors(tmp))
            elif s == 'subject':
                epub_metadata[s] = ', '.join(tmp)
            elif s == 'date':
                epub_metadata[s] = tmp[0][:10]
            else:
                epub_metadata[s] = tmp[0]
        else:
            epub_metadata[s] = 'Unknown'

    if epub_metadata['subject'] == 'Unknown':
        epub_metadata['subject'] = ''

    if epub_metadata['publisher'] == u'Unknown':
        epub_metadata['publisher'] = ''

    if epub_metadata['date'] == u'Unknown':
        epub_metadata['date'] = ''

    if epub_metadata['description'] == u'Unknown':
        description = tree.xpath("//*[local-name() = 'description']/text()")
        if len(description) > 0:
            epub_metadata['description'] = description
        else:
            epub_metadata['description'] = ""

    lang = epub_metadata['language'].split('-', 1)[0].lower()
    epub_metadata['language'] = lang

    epub_metadata = parse_epub_series(ns, tree, epub_metadata)

    cover_file = parse_epub_cover(ns, tree, epub_zip, cover_path, tmp_file_path)

    identifiers = []
    for node in p.xpath('dc:identifier', namespaces=ns):
        identifier_name=node.attrib.values()[-1];
        identifier_value=node.text;
        if identifier_name in ('uuid','calibre'):
            continue;
        identifiers.append( [identifier_name, identifier_value] )

    if not epub_metadata['title']:
        title = original_file_name
    else:
        title = epub_metadata['title']

    return {
        "file_path": tmp_file_path,
        "extension": original_file_extension,
        "title": title.encode('utf-8').decode('utf-8'),
        "author": epub_metadata['creator'].encode('utf-8').decode('utf-8'),
        "cover": cover_file,
        "description": epub_metadata['description'],
        "tags": epub_metadata['subject'].encode('utf-8').decode('utf-8'),
        "series": epub_metadata['series'].encode('utf-8').decode('utf-8'),
        "series_id": epub_metadata['series_id'].encode('utf-8').decode('utf-8'),
        "languages": epub_metadata['language'],
        "publisher": epub_metadata['publisher'].encode('utf-8').decode('utf-8'),
        "pubdate": epub_metadata['date'],
        "identifiers": identifiers
    }


def parse_epub_cover(ns, tree, epub_zip, cover_path, tmp_file_path):
    cover_section = tree.xpath("/pkg:package/pkg:manifest/pkg:item[@id='cover-image']/@href", namespaces=ns)
    cover_file = None
    # if len(cover_section) > 0:
    if not cover_file:
        meta_cover = tree.xpath("/pkg:package/pkg:metadata/pkg:meta[@name='cover']/@content", namespaces=ns)
        if len(meta_cover) > 0:
            cover_section = tree.xpath(
                "/pkg:package/pkg:manifest/pkg:item[@id='"+meta_cover[0]+"']/@href", namespaces=ns)
            if not cover_section:
                cover_section = tree.xpath(
                    "/pkg:package/pkg:manifest/pkg:item[@properties='" + meta_cover[0] + "']/@href", namespaces=ns)
        else:
            cover_section = tree.xpath("/pkg:package/pkg:guide/pkg:reference/@href", namespaces=ns)
        for cs in cover_section:
            filetype = cs.rsplit('.', 1)[-1]
            if filetype == "xhtml" or filetype == "html":  # if cover is (x)html format
                markup = epub_zip.read(os.path.join(cover_path, cs))
                markup_tree = etree.fromstring(markup)
                # no matter xhtml or html with no namespace
                img_src = markup_tree.xpath("//*[local-name() = 'img']/@src")
                # Alternative image source
                if not len(img_src):
                    img_src = markup_tree.xpath("//attribute::*[contains(local-name(), 'href')]")
                if len(img_src):
                    # img_src maybe start with "../"" so fullpath join then relpath to cwd
                    filename = os.path.relpath(os.path.join(os.path.dirname(os.path.join(cover_path, cover_section[0])),
                                                            img_src[0]))
            if cover_file: break
    return cover_file


def parse_epub_series(ns, tree, epub_metadata):
    series = tree.xpath("/pkg:package/pkg:metadata/pkg:meta[@name='calibre:series']/@content", namespaces=ns)
    if len(series) > 0:
        epub_metadata['series'] = series[0]
    else:
        epub_metadata['series'] = ''

    series_id = tree.xpath("/pkg:package/pkg:metadata/pkg:meta[@name='calibre:series_index']/@content", namespaces=ns)
    if len(series_id) > 0:
        epub_metadata['series_id'] = series_id[0]
    else:
        epub_metadata['series_id'] = '1'
    return epub_metadata
