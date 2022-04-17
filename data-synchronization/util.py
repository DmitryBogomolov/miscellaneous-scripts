import os
import os.path as path
import subprocess

def check_dir_exist(dir_path):
    if not path.isdir(dir_path):
        raise RuntimeError('"{}" does not exist'.format(dir_path))

def call_proc(proc_args, capture_output=False, cwd=None):
    return subprocess.run(proc_args, encoding='utf8', check=True, capture_output=capture_output, cwd=cwd)

def get_disk_path(disk_name):
    return path.join('/media', os.getenv('USER'), disk_name)

def is_dry_run(dry_run):
    return dry_run or os.getenv('SYNC_DRY_RUN')
