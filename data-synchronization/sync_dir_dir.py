#!/usr/bin/env python3

import sys
import argparse
import os
from os import path
import subprocess

def check_dir(dir_path):
    if not path.isdir(dir_path):
        raise ValueError('{} is not a directory'.format(dir_path))

def main():
    parser = argparse.ArgumentParser(
        description='Synchronizes directories with rsync util.'
    )
    parser.add_argument('src_dir', help='source directory')
    parser.add_argument('dst_dir', help='target directory')
    parser.add_argument('--dry-run', action='store_true', help='do dry run')
    args = parser.parse_args(sys.argv[1:])

    src_dir = path.abspath(args.src_dir) + '/'
    dst_dir = path.abspath(args.dst_dir) + '/'

    check_dir(src_dir)
    check_dir(dst_dir)
    proc_args = ['rsync', '--archive', '--delete', '--compress', '--progress', '-v', '-h']
    if args.dry_run or os.getenv('SYNC_DRY_RUN'):
        proc_args.append('--dry-run')

    proc_args.append(src_dir)
    proc_args.append(dst_dir)
    subprocess.run(
        proc_args,
        encoding='utf8', check=True
    )

if __name__ == '__main__':
    main()
