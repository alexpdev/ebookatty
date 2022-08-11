def main():
    parser = ArgumentParser(description="get ebook metadata")
    parser.add_argument('file', type=str, help='path to ebook file(s), standard file pattern extensions are allowed.', nargs="+")
    parser.add_argument('-r', '--recursive', help='recusively search for given file patterns')
    parser.add_argument('-o', '--output', help='file path where metadata will be written. Acceptable formats include json and csv and are determined based on the file extension. Default is None', action="store")
    args = parser.parse_args(sys.argv[1:])

    get_metadata(args.path)
