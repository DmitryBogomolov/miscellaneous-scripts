import sys
import argparse
import os
from os import path
import subprocess
import time

DRY_RUN_ENV = 'SYNC_DRY_RUN'

def check_dir_exist(dir_path):
    if not path.isdir(dir_path):
        raise RuntimeError('"{}" directory does not exist'.format(dir_path))

def check_file_exist(file_path):
    if not path.isfile(file_path):
        raise RuntimeError('"{}" file does not exist'.format(file_path))

def call_proc(proc_args, capture_output=False, cwd=None):
    kwargs = dict(encoding='utf8', check=True, cwd=cwd)
    if capture_output:
        kwargs['stdout'] = subprocess.PIPE
        kwargs['stderr'] = subprocess.PIPE
    return subprocess.run(proc_args, **kwargs)

def get_disk_path(disk_name):
    return path.join('/media', os.getenv('USER'), disk_name)

def is_dry_run(dry_run):
    return dry_run or os.getenv(DRY_RUN_ENV)

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
    try:
        func()
    finally:
        end_time = time.time()
        duration = int(end_time - begin_time)
        print('time: {}s'.format(duration))
