#!/usr/bin/env python3

from os import path
import util

def sync_dir_dir(src_path: str, dst_path: str, dry_run: bool) -> None:
    src_dir = path.abspath(src_path) + '/'
    dst_dir = path.abspath(dst_path) + '/'
    is_dry_run = util.is_dry_run(dry_run)

    util.check_dir_exist(src_dir)
    util.check_dir_exist(dst_dir)
    check_dirs_intersection(src_dir, dst_dir)
    proc_args = ['rsync', '--archive', '--delete', '--compress', '--progress', '-v', '-h']
    if is_dry_run:
        proc_args.append('--dry-run')
    proc_args.append(src_dir)
    proc_args.append(dst_dir)

    util.call_proc(proc_args)

def check_dirs_intersection(src_dir: str, dst_dir: str) -> None:
    if src_dir.startswith(dst_dir) or dst_dir.startswith(src_dir):
        raise ValueError(f'directories "{src_dir}" and "{dst_dir}" intersect')

def main() -> None:
    def setup_args(parser: util.ArgumentParser) -> None:
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
