#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""ebookatty Package."""

import sys
from pathlib import Path
sys.path.insert(0,Path(__file__).resolve().parent.parent)

from ebookatty.atty import MetadataFetcher, get_metadata


__version__ = "0.2.0"

__all__ = [MetadataFetcher, get_metadata]
