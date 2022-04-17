import os
import os.path as path
import subprocess

def check_dir_exist(dir_path):
    if not path.isdir(dir_path):
        raise RuntimeError('"{}" does not exist'.format(dir_path))

def call_proc(args):
    subprocess.run(args, encoding='utf8', check=True)

def get_disk_path(disk_name):
    return path.join('/media', os.getenv('USER'), disk_name)
