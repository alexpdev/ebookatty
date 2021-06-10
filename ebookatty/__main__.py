import os,sys
from pathlib import Path
sys.path.insert(0,Path(__file__).resolve().parent.parent)
from argparse import ArgumentParser
from ebookatty.atty import MetadataFetcher, get_metadata

if __name__ == "__main__":
    parser = ArgumentParser(description="get ebook metadata")

    parser.add_argument('path', type=str,help='path to ebook file')
    args = parser.parse_args()
    print(get_metadata(args.path))

# parser.add_argument("path", nargs="+", help="path to ebook")
# parser.add_argument(
#         "-d", "--directory", action="append", help="path to ebooks directory"
#     )
#     paths = parser.parse_args(sys.argv[1:])
#     if paths.directory:
#         d = [Path(i) for i in paths.directory]
#         for path in d:
#             for item in path.iterdir():
#                 print(format_output(get_metadata(item)))
