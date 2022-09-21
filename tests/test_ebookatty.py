import sys
import shutil
import os
import pytest
from ebookatty import MetadataFetcher
from ebookatty.__main__ import main
from ebookatty.cli import execute


def get_testfiles():
    parent = os.path.dirname(__file__)
    testbooks = os.path.join(parent, "testbooks")
    lst = [os.path.join(testbooks, i) for i in os.listdir(testbooks)]
    return lst


@pytest.fixture
def testdir():
    base = os.path.dirname(__file__)
    testbooks = os.path.join(base, "testbooks")
    return testbooks


@pytest.fixture(scope="module")
def outdir():
    base = os.path.dirname(__file__)
    odir = os.path.join(base, "outdir")
    if not os.path.exists(odir):
        os.mkdir(odir)
    yield odir
    shutil.rmtree(odir)


@pytest.mark.parametrize("book", get_testfiles())
def test_get_metadata(book):
    assert MetadataFetcher(book).get_metadata() is not None


@pytest.mark.parametrize("book", get_testfiles())
def test_metadata_fetcher(book):
    fetcher = MetadataFetcher(book)
    assert fetcher.get_metadata() is not None



@pytest.mark.parametrize("pattern", ["*.epub", "*.azw3", "*.mobi"])
@pytest.mark.parametrize("ext", [".csv", ".json"])
@pytest.mark.parametrize("flag", ["-o", "--output", ""])
def test_cli(testdir, flag, outdir, pattern, ext):
    """Test the cli."""
    files = os.path.join(testdir, pattern)
    args = ["ebookatty", files]
    out = ""
    if flag:
        out = os.path.join(outdir, "outfile" + ext)
        args += [flag, out]
    sys.argv = args
    execute()
    if flag:
        assert os.path.exists(out)
    else:
        assert not out


def test_main_execute():
    import sys
    args = ["ebookatty"]
    sys.argv = args
    try:
        result = main()
    except SystemExit:
        assert True
