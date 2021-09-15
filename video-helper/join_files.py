#!/usr/bin/env python3

import os
from os import path

def join_files(first_file: str) -> None:
    src_file = path.abspath(first_file)
    if not path.isfile(src_file):
        raise RuntimeError('file "{0}" does not exist'.format(src_file))

    dir_path = path.dirname(src_file)
    first_name = path.basename(src_file)
    items = os.listdir(dir_path)
    items.sort()
    i0 = items.index(first_name)
    for i in range(i0, len(items)):
        pass

def main():
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Joins mp4 files')
    parser.add_argument('file_name', type=str)
    args = parser.parse_args(sys.argv[1:])
    join_files(args.file_name)

if __name__ == '__main__':
    main()
