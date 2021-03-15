from pathlib import Path
from src.epubmeta import EpubMeta
from src.kindlemeta import KindleMeta
from src.mobimeta import MobiMeta

class EbookMetadata:
    def __init__(self,path):
        self.path = Path(path)
        self.metadata = []
        if self.path.suffix == ".mobi":
            self.meta = MobiMeta(self.path)
        elif self.path.suffix == ".epub":
            self.meta = EpubMeta(self.path)
        elif self.path.suffix in [".azw3","azw","kfx"]:
            self.meta = KindleMeta(self.path)
        self.metadata = self.meta.metadata

    def get_metadata(self):
        return self.meta.get_metadata()

class PathDoesNotExistError(Exception):
    pass


def get_metadata(path):
    if isinstance(path,str):
        path = Path(path)


    if not path.exists():
        raise PathDoesNotExistError

    if path.suffix in [".mobi",".azw3",".azw",".kfx",".epub"]:
        reader = EbookMetadata(path)
        return reader.get_metadata()


