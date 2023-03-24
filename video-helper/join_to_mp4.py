#!/usr/bin/env python3

from typing import List
from join_files import join_files
from to_mp4_many import to_mp4_many

def convert_and_join(file_names: List[str], out_file: str) -> None:
    mp4_file_names = to_mp4_many(file_names, len(file_names))
    join_files(mp4_file_names, out_file)

def main() -> None:
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Converts files to .mp4 and joins them')
    parser.add_argument(
        'file_names', type=str, nargs='+',
        help='files to join'
    )
    parser.add_argument(
        '--out-file', type=str, required=True, dest='out_file',
        help='joined file'
    )
    args = parser.parse_args(sys.argv[1:])

    convert_and_join(args.file_names, args.out_file)

if __name__ == '__main__':
    main()
