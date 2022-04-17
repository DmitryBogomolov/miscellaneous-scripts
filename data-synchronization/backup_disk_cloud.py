#!/usr/bin/env python3

import os.path as path
import util

def backup_dir(dir_path, bucket_path, dir_name, is_dry_run, tool_name):
    src_path = path.join(dir_path, dir_name)
    dst_path = bucket_path + '/' + dir_name
    print('### "{}" --> "{}"'.format(src_path, dst_path))
    proc_args = [tool_name, 's3', 'sync', '--delete']
    if is_dry_run:
        proc_args.append('--dryrun')
    proc_args.append(src_path)
    proc_args.append(dst_path)
    util.call_proc(proc_args)
    print('')

def backup_disk_cloud(disk, bucket, dry_run, tool_name):
    disk_path = util.get_disk_path(disk)
    bucket_path = 's3://' + bucket
    is_dry_run = util.is_dry_run(dry_run)

    util.check_dir_exist(disk_path)
    target_dirs = util.read_list_file(path.join(disk_path, '.backup_disk_cloud'))

    for dir_name in target_dirs:
        backup_dir(disk_path, bucket_path, dir_name, is_dry_run, tool_name)

def main():
    def setup_args(parser):
        parser.add_argument('disk', help='source disk name')
        parser.add_argument('bucket', help='target bucket name')
        parser.add_argument('--tool', default='aws', help='s3 tool to use')
    args = util.parse_cmd_args(
        'Synchronizes disk to s3 bucket.',
        setup_args,
        add_dry_run=True
    )

    util.measure_time(lambda: backup_disk_cloud(args.disk, args.bucket, args.dry_run, args.tool))

if __name__ == '__main__':
    main()
