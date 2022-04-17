#!/usr/bin/env python3

import os.path as path
import util

def sync_dir_dir(src_path, dst_path, dry_run):
    src_dir = path.abspath(src_path) + '/'
    dst_dir = path.abspath(dst_path) + '/'
    is_dry_run = util.is_dry_run(dry_run)

    util.check_dir_exist(src_dir)
    util.check_dir_exist(dst_dir)
    proc_args = ['rsync', '--archive', '--delete', '--compress', '--progress', '-v', '-h']
    if is_dry_run:
        proc_args.append('--dry-run')
    proc_args.append(src_dir)
    proc_args.append(dst_dir)

    util.call_proc(proc_args)

def main():
    def setup_args(parser):
        parser.add_argument('src_dir', help='source directory')
        parser.add_argument('dst_dir', help='target directory')
    args = util.parse_cmd_args(
        'Synchronizes directories with rsync util.',
        setup_args,
        add_dry_run=True
    )

    sync_dir_dir(args.src_dir, args.dst_dir, args.dry_run)

if __name__ == '__main__':
    main()
