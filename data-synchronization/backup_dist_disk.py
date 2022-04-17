#!/usr/bin/env python3

import sys
import argparse
import os.path as path
import time
import util
import sync_dir_dir

def sync_dirs(src_dir, dst_dir, dir_name, dry_run):
    src = path.join(src_dir, dir_name)
    dst = path.join(dst_dir, dir_name)
    print('### "{}" --> "{}"'.format(src, dst))
    sync_dir_dir.sync_dir_dir(src, dst, dry_run)
    print('')

def backup_disk_disk(src_disk, dst_disk, dry_run):
    src_path = util.get_disk_path(src_disk)
    dst_path = util.get_disk_path(dst_disk)

    util.check_dir_exist(src_path)
    util.check_dir_exist(dst_path)

    list_file_path = path.join(src_path, '.backup_disk_disk')
    if not path.isfile(list_file_path):
        raise RuntimeError('"{}" does not exist'.format(list_file_path))

    with open(list_file_path, 'r', encoding='utf8') as file_buffer:
        target_dirs = [line.strip() for line in file_buffer.readlines()]

    begin_time = time.time()
    for target_dir in target_dirs:
        sync_dirs(src_path, dst_path, target_dir, dry_run)
    end_time = time.time()
    duration = int(end_time - begin_time)
    print('time: {}s'.format(duration))

def main():
    parser = argparse.ArgumentParser(
        description='Synchronizes disks.'
    )
    parser.add_argument('src_disk', help='source disk')
    parser.add_argument('dst_disk', help='target disk')
    parser.add_argument('--dry-run', action='store_true', help='do dry run')
    args = parser.parse_args(sys.argv[1:])

    backup_disk_disk(args.src_disk, args.dst_disk, args.dry_run)

if __name__ == '__main__':
    main()
