#!/usr/bin/env python3

from os import path
import util
import sync_dir_dir

LIST_FILE_NAME = '.backup_disk_disk'

def sync_dirs(src_dir: str, dst_dir: str, dir_name: str, dry_run: bool) -> None:
    src = path.join(src_dir, dir_name)
    dst = path.join(dst_dir, dir_name)
    print(f'### "{src}" --> "{dst}"')
    sync_dir_dir.sync_dir_dir(src, dst, dry_run)
    print('')

def backup_disk_disk(src_disk: str, dst_disk: str, dry_run: bool) -> None:
    src_path = util.get_disk_path(src_disk)
    dst_path = util.get_disk_path(dst_disk)

    util.check_dir_exist(src_path)
    util.check_dir_exist(dst_path)
    target_dirs = util.read_list_file(path.join(src_path, LIST_FILE_NAME))

    for target_dir in target_dirs:
        sync_dirs(src_path, dst_path, target_dir, dry_run)

def main() -> None:
    def setup_args(parser: util.ArgumentParser) -> None:
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
