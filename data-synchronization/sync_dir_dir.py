#!/usr/bin/env python3

from pickletools import uint1
import sys
import argparse
import os
import os.path as path
import util

def sync_dir_dir(src_path, dst_path, dry_run):
    src_dir = path.abspath(src_path) + '/'
    dst_dir = path.abspath(dst_path) + '/'
    dry_run = dry_run or os.getenv('SYNC_DRY_RUN')

    util.check_dir_exist(src_dir)
    util.check_dir_exist(dst_dir)
    proc_args = ['rsync', '--archive', '--delete', '--compress', '--progress', '-v', '-h']
    if dry_run:
        proc_args.append('--dry-run')
    proc_args.append(src_dir)
    proc_args.append(dst_dir)

    util.call_proc(proc_args)

def main():
    parser = argparse.ArgumentParser(
        description='Synchronizes directories with rsync util.'
    )
    parser.add_argument('src_dir', help='source directory')
    parser.add_argument('dst_dir', help='target directory')
    parser.add_argument('--dry-run', action='store_true', help='do dry run')
    args = parser.parse_args(sys.argv[1:])

    sync_dir_dir(args.src_dir, args.dst_dir, args.dry_run)

if __name__ == '__main__':
    main()
