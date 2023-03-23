from typing import List, Callable, Any, Optional
import sys
from argparse import ArgumentParser, Namespace
import os
from os import path
import subprocess
import time
import tempfile

DRY_RUN_ENV = 'SYNC_DRY_RUN'

def normalize_path_arg(raw_path: str) -> str:
    return raw_path and path.abspath(raw_path)

def make_tmp_dir(output_path: str) -> tempfile.TemporaryDirectory:
    return tempfile.TemporaryDirectory(dir=path.dirname(output_path))

def check_dir_exist(dir_path: str) -> None:
    if not path.isdir(dir_path):
        raise NotADirectoryError(f'"{dir_path}" directory does not exist')

def check_file_exist(file_path: str) -> None:
    if not path.isfile(file_path):
        raise FileNotFoundError(f'"{file_path}" file does not exist')

def call_proc(
    proc_args: List[str],
    capture_output: bool = False,
    cwd: Optional[str] = None,
) -> subprocess.CompletedProcess:
    kwargs: Any = {}
    if capture_output:
        kwargs['stdout'] = subprocess.PIPE
        kwargs['stderr'] = subprocess.PIPE
    return subprocess.run(proc_args, encoding='utf8', check=True, cwd=cwd, **kwargs)

def get_disk_path(disk_name: str) -> str:
    return path.join(path.expandvars('/media/$USER'), disk_name)

def is_dry_run(dry_run: bool) -> bool:
    return dry_run or bool(os.getenv(DRY_RUN_ENV))

def read_list_file(file_path: str) -> List[str]:
    check_file_exist(file_path)
    with open(file_path, 'r', encoding='utf8') as file_obj:
        return [line.strip() for line in file_obj.readlines()]

def parse_cmd_args(
    description: str,
    setup_args: Callable[[ArgumentParser], None],
    add_dry_run: bool = False,
) -> Namespace:
    parser = ArgumentParser(description=description)
    setup_args(parser)
    if add_dry_run:
        parser.add_argument('--dry-run', action='store_true', help='do dry run')
    return parser.parse_args(sys.argv[1:])

def measure_time(func: Callable) -> None:
    begin_time = time.time()
    try:
        func()
    finally:
        end_time = time.time()
        duration = int(end_time - begin_time)
        print(f'time: {duration}s')
