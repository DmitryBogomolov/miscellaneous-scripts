#!/usr/bin/env python3

import os
from os import path

def join_files(file_names):
    pass

def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Joins mp4 files')
    parser.add_argument('file_names', type=str, nargs='+', help='files to join')
    args = parser.parse_args(sys.argv[1:])

    join_files(args.file_names)

if __name__ == '__main__':
    main()
