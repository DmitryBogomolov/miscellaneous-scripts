import sys
import argparse
import os
import os.path as path
import subprocess
import time

def check_dir_exist(dir_path):
    if not path.isdir(dir_path):
        raise RuntimeError('"{}" directory does not exist'.format(dir_path))

def check_file_exist(file_path):
    if not path.isfile(file_path):
        raise RuntimeError('"{}" file does not exist'.format(file_path))

def call_proc(proc_args, capture_output=False, cwd=None):
    return subprocess.run(
        proc_args,
        encoding='utf8', check=True, capture_output=capture_output, cwd=cwd
    )

def get_disk_path(disk_name):
    return path.join('/media', os.getenv('USER'), disk_name)

def is_dry_run(dry_run):
    return dry_run or os.getenv('SYNC_DRY_RUN')

def read_list_file(file_path):
    check_file_exist(file_path)
    with open(file_path, 'r', encoding='utf8') as file_buffer:
        return [line.strip() for line in file_buffer.readlines()]

def parse_cmd_args(description, setup_args, add_dry_run=False):
    parser = argparse.ArgumentParser(description=description)
    setup_args(parser)
    if add_dry_run:
        parser.add_argument('--dry-run', action='store_true', help='do dry run')
    return parser.parse_args(sys.argv[1:])

def measure_time(func):
    begin_time = time.time()
    func()
    end_time = time.time()
    duration = int(end_time - begin_time)
    print('time: {}s'.format(duration))
