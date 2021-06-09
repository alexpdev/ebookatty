#! /usr/bin/python3
# -*- coding: utf-8 -*-

########################################################################
#  Copyright (C) 2021  alexpdev
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
###############################################################################
"""Parsing Utilities."""
from pathlib import Path


class HeaderMissingError(Exception):
    """Raise HeaderMissingError."""

    pass


class MetadataError(HeaderMissingError):
    """Raise MetadataError."""

    pass


def path_meta(path):
    """
    Metadata extracted from the file and path names.

    Args:
        path (str): path to file

    Returns:
        dict: key, value pairs of metadata parsed.
    """
    if isinstance(path, str):
        path = Path(path)
    metadata = [
        ("filename", path.name),
        ("path", str(path)),
        ("extension", path.suffix),
        ("size", path.stat().st_size),
    ]
    return metadata


def reverse_tag_iter(block):
    """
    Decode tag names.

    Args:
        block (bytes): tag names

    Yields:
        str: tag name
    """
    end = len(block)
    while True:
        pgt = block.rfind(b">", 0, end)
        if pgt == -1:
            break
        plt = block.rfind(b"<", 0, pgt)
        if plt == -1:
            break
        yield block[plt : pgt + 1]
        end = plt


def getLanguage(langID, sublangID):
    """
    Get Language Standard.

    Args:
        langID (str): Landguage ID
        sublangID (str): Sublanguage ID

    Returns:
        str: Language encoding.
    """
    langdict = {
        54: {0: "af"},  # Afrikaans
        28: {0: "sq"},  # Albanian
        1: {
            0: "ar",
            5: "ar-dz",
            15: "ar-bh",
            3: "ar-eg",
            2: "ar-iq",
            11: "ar-jo",
            13: "ar-kw",
            12: "ar-lb",
            4: "ar-ly",
            6: "ar-ma",
            8: "ar-om",
            16: "ar-qa",
            1: "ar-sa",
            10: "ar-sy",
            7: "ar-tn",
            14: "ar-ae",
            9: "ar-ye",
        },  # Arabic
        43: {0: "hy"},  # Armenian
        77: {0: "as"},  # Assamese
        44: {0: "az"},  # "Azeri (IANA: Azerbaijani)
        45: {0: "eu"},  # Basque
        35: {0: "be"},  # Belarusian
        69: {0: "bn"},  # Bengali
        2: {0: "bg"},  # Bulgarian
        3: {0: "ca"},  # Catalan
        # Chinese
        4: {0: "zh", 3: "zh-hk", 2: "zh-cn", 4: "zh-sg", 1: "zh-tw"},
        26: {0: "hr", 3: "sr"},  # Croatian, Serbian
        5: {0: "cs"},  # Czech
        6: {0: "da"},  # Danish
        # Dutch / Flemish,  Dutch (Belgium)
        19: {0: "nl", 1: "nl", 2: "nl-be"},
        9: {
            0: "en",
            1: "en",
            3: "en-au",
            40: "en-bz",
            4: "en-ca",
            6: "en-ie",
            8: "en-jm",
            5: "en-nz",
            13: "en-ph",
            7: "en-za",
            11: "en-tt",
            2: "en-gb",
            1: "en-us",
            12: "en-zw",
        },  # English
        37: {0: "et"},  # Estonian
        56: {0: "fo"},  # Faroese
        41: {0: "fa"},  # Farsi / Persian
        11: {0: "fi"},  # Finnish
        12: {
            0: "fr",
            1: "fr",
            2: "fr-be",
            3: "fr-ca",
            5: "fr-lu",
            6: "fr-mc",
            4: "fr-ch",
        },  # French
        55: {0: "ka"},  # Georgian
        # German
        7: {0: "de", 1: "de", 3: "de-at", 5: "de-li", 4: "de-lu", 2: "de-ch"},
        8: {0: "el"},  # Greek, Modern (1453-)
        71: {0: "gu"},  # Gujarati
        13: {0: "he"},  # Hebrew (also code 'iw'?)
        57: {0: "hi"},  # Hindi
        14: {0: "hu"},  # Hungarian
        15: {0: "is"},  # Icelandic
        33: {0: "id"},  # Indonesian
        16: {0: "it", 1: "it", 2: "it-ch"},  # Italian,  Italian (Switzerland)
        17: {0: "ja"},  # Japanese
        75: {0: "kn"},  # Kannada
        63: {0: "kk"},  # Kazakh
        87: {0: "x-kok"},  # Konkani (real language code is 'kok'?)
        18: {0: "ko"},  # Korean
        38: {0: "lv"},  # Latvian
        39: {0: "lt"},  # Lithuanian
        47: {0: "mk"},  # Macedonian
        62: {0: "ms"},  # Malay
        76: {0: "ml"},  # Malayalam
        58: {0: "mt"},  # Maltese
        78: {0: "mr"},  # Marathi
        97: {0: "ne"},  # Nepali
        20: {0: "no"},  # Norwegian
        72: {0: "or"},  # Oriya
        21: {0: "pl"},  # Polish
        22: {0: "pt", 2: "pt", 1: "pt-br"},  # Portuguese,  Portuguese (Brazil)
        70: {0: "pa"},  # Punjabi
        23: {0: "rm"},  # "Rhaeto-Romanic" (IANA: Romansh)
        24: {0: "ro"},  # Romanian
        25: {0: "ru"},  # Russian
        59: {0: "sz"},  # "Sami (Lappish)" (not an IANA language code)
        79: {0: "sa"},  # Sanskrit
        27: {0: "sk"},  # Slovak
        36: {0: "sl"},  # Slovenian
        46: {0: "sb"},  # "Sorbian" (not an IANA language code)
        10: {
            0: "es",
            4: "es",
            44: "es-ar",
            64: "es-bo",
            52: "es-cl",
            36: "es-co",
            20: "es-cr",
            28: "es-do",
            48: "es-ec",
            68: "es-sv",
            16: "es-gt",
            72: "es-hn",
            8: "es-mx",
            76: "es-ni",
            24: "es-pa",
            60: "es-py",
            40: "es-pe",
            80: "es-pr",
            56: "es-uy",
            32: "es-ve",
        },  # Spanish
        48: {0: "sx"},  # "Sutu" (not an IANA language code)
        65: {0: "sw"},  # Swahili
        29: {0: "sv", 1: "sv", 8: "sv-fi"},  # Swedish,  Swedish (Finland)
        73: {0: "ta"},  # Tamil
        68: {0: "tt"},  # Tatar
        74: {0: "te"},  # Telugu
        30: {0: "th"},  # Thai
        49: {0: "ts"},  # Tsonga
        50: {0: "tn"},  # Tswana
        31: {0: "tr"},  # Turkish
        34: {0: "uk"},  # Ukrainian
        32: {0: "ur"},  # Urdu
        67: {0: "uz", 2: "uz"},  # Uzbek
        42: {0: "vi"},  # Vietnamese
        52: {0: "xh"},  # Xhosa
        53: {0: "zu"},  # Zulu
    }
    sublangID = 0 if not sublangID else sublangID
    try:
        lang = langdict[langID][sublangID]
    except KeyError:
        lang = "en"
    return lang
