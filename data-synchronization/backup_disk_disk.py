#!/usr/bin/env python3

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
    target_dirs = util.read_list_file(path.join(src_path, '.backup_disk_disk'))

    for target_dir in target_dirs:
        sync_dirs(src_path, dst_path, target_dir, dry_run)

def main():
    def setup_args(parser):
        parser.add_argument('src_disk', help='source disk name')
        parser.add_argument('dst_disk', help='target disk name')
    args = util.parse_cmd_args(
        'Synchronizes disk to disk.',
        setup_args,
        add_dry_run=True
    )

    util.measure_time(lambda: backup_disk_disk(args.src_disk, args.dst_disk, args.dry_run))

if __name__ == '__main__':
    main()
