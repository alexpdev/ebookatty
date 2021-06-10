#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""ebookatty Package."""


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
#########################################################################

from ebookatty.atty import MetadataFetcher, get_metadata
from ebookatty.epubmeta import EpubMeta
from ebookatty.mobimeta import MobiMeta
from ebookatty.kindlemeta import KindleMeta

__version__ = "0.2.0"

__all__ = [MetadataFetcher, get_metadata, KindleMeta, MobiMeta, EpubMeta]
