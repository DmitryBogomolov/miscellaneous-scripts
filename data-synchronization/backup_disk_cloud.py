#!/usr/bin/env python3

from os import path
import util

LIST_FILE_NAME = '.backup_disk_cloud'

def backup_dir(
    dir_path: str, bucket_path: str, dir_name: str, tool_name: str, is_dry_run: bool
) -> None:
    src_path = path.join(dir_path, dir_name)
    dst_path = bucket_path + '/' + dir_name
    print(f'### "{src_path}" --> "{dst_path}"')
    proc_args = [tool_name, 's3', 'sync', '--delete']
    if is_dry_run:
        proc_args.append('--dryrun')
    proc_args.append(src_path)
    proc_args.append(dst_path)
    util.call_proc(proc_args)
    print('')

def backup_disk_cloud(disk: str, bucket: str, tool_name: str, dry_run: bool) -> None:
    disk_path = util.get_disk_path(disk)
    bucket_path = 's3://' + bucket
    is_dry_run = util.is_dry_run(dry_run)

    util.check_dir_exist(disk_path)
    target_dirs = util.read_list_file(path.join(disk_path, LIST_FILE_NAME))

    for dir_name in target_dirs:
        backup_dir(disk_path, bucket_path, dir_name, tool_name, is_dry_run)

def main() -> None:
    def setup_args(parser: util.ArgumentParser) -> None:
        parser.add_argument('disk', help='source disk name')
        parser.add_argument('bucket', help='target bucket name')
        parser.add_argument('--tool', default='aws', help='s3 tool to use')
    args = util.parse_cmd_args(
        'Synchronizes disk to s3 bucket.',
        setup_args,
        add_dry_run=True
    )

    util.measure_time(lambda: backup_disk_cloud(args.disk, args.bucket, args.tool, args.dry_run))

if __name__ == '__main__':
    main()
