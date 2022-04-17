#!/usr/bin/env python3

import sys
import argparse
import os.path as path
import time
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

    begin_time = time.time()
    for dir_name in target_dirs:
        backup_dir(disk_path, bucket_path, dir_name, is_dry_run, tool_name)
    end_time = time.time()
    duration = int(end_time - begin_time)
    print('time: {}s'.format(duration))

def main():
    parser = argparse.ArgumentParser(
        description='Synchronizes disk to s3 bucket.'
    )
    parser.add_argument('disk', help='source disk name')
    parser.add_argument('bucket', help='target bucket name')
    parser.add_argument('--tool', default='aws', help='s3 tool to use')
    parser.add_argument('--dry-run', action='store_true', help='do dry run')
    args = parser.parse_args(sys.argv[1:])

    backup_disk_cloud(args.disk, args.bucket, args.dry_run, args.tool)

if __name__ == '__main__':
    main()
