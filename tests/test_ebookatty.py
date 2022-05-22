import os
import pytest
from ebookatty import get_metadata, MetadataFetcher

def get_testfiles():
    parent = os.path.dirname(__file__)
    testbooks = os.path.join(parent, "testbooks")
    lst = [os.path.join(testbooks, i) for i in os.listdir(testbooks)]
    return lst


@pytest.mark.parametrize("book", get_testfiles())
def test_get_metadata(book):
    assert get_metadata(book) is not None


@pytest.mark.parametrize("book", get_testfiles())
def test_metadata_fetcher(book):
    fetcher = MetadataFetcher(book)
    assert fetcher.get_metadata() is not None
