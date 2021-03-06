import sys
import argparse
import os
from os import path
import subprocess
import time
import tempfile

DRY_RUN_ENV = 'SYNC_DRY_RUN'

def normalize_path_arg(raw_path):
    return raw_path and path.abspath(raw_path)

def make_tmp_dir(output_path):
    return tempfile.TemporaryDirectory(dir=path.dirname(output_path))

def check_dir_exist(dir_path):
    if not path.isdir(dir_path):
        raise NotADirectoryError('"{}" directory does not exist'.format(dir_path))

def check_file_exist(file_path):
    if not path.isfile(file_path):
        raise FileNotFoundError('"{}" file does not exist'.format(file_path))

def call_proc(proc_args, capture_output = False, cwd = None):
    kwargs = {}
    if capture_output:
        kwargs['stdout'] = subprocess.PIPE
        kwargs['stderr'] = subprocess.PIPE
    return subprocess.run(proc_args, encoding='utf8', check=True, cwd=cwd, **kwargs)

def get_disk_path(disk_name):
    return path.join(path.expandvars('/media/$USER'), disk_name)

def is_dry_run(dry_run):
    return dry_run or bool(os.getenv(DRY_RUN_ENV))

def read_list_file(file_path):
    check_file_exist(file_path)
    with open(file_path, 'r', encoding='utf8') as file_obj:
        return [line.strip() for line in file_obj.readlines()]

def parse_cmd_args(description, setup_args, add_dry_run = False):
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
