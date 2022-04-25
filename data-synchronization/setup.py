#!/usr/bin/env python3

import os
from os import path
import stat
import shutil
import util

LIB_DIR = path.join(os.getenv('HOME'), '.local/lib/data-synchronization')
BIN_DIR = path.join(os.getenv('HOME'), '.local/bin')

def is_executable(file_path):
    with open(file_path, 'r', encoding='utf8') as file_buffer:
        line = file_buffer.readline().strip()
        return line.startswith('#!/usr/bin/env')

def install():
    target_dir = path.dirname(path.abspath(__file__))
    target_files = []
    executables = []
    for item in os.listdir(target_dir):
        if path.isfile(item) and item.endswith('.py') and item != __file__:
            target_files.append(item)
            if is_executable(path.join(target_dir, item)):
                executables.append(item)

    shutil.rmtree(LIB_DIR, ignore_errors=True)
    os.makedirs(LIB_DIR, exist_ok=True)
    for item in target_files:
        shutil.copy2(path.join(target_dir, item), path.join(LIB_DIR, item))

    for item in executables:
        full_path = path.join(LIB_DIR, item)
        os.chmod(full_path, os.stat(full_path).st_mode | stat.S_IEXEC)

    for item in executables:
        src_path = path.join(LIB_DIR, item)
        dst_path = path.join(BIN_DIR, item[:-3])    # strip .py extension
        if path.exists(dst_path) and path.realpath(dst_path) != src_path:
            os.remove(dst_path)
        if not path.exists(dst_path):
            os.symlink(src_path, dst_path)

def uninstall():
    for item in os.listdir(BIN_DIR):
        full_path = path.join(BIN_DIR, item)
        if path.islink(full_path):
            real_path = path.realpath(full_path)
            if real_path.startswith(LIB_DIR):
                os.remove(full_path)
    shutil.rmtree(LIB_DIR, ignore_errors=True)

def main():
    def setup_args(parser):
        parser.add_argument('mode', choices=['on', 'off'], help='Add or remove scripts')
    args = util.parse_cmd_args(
        'Manages scripts',
        setup_args
    )

    if args.mode == 'on':
        install()
    if args.mode == 'off':
        uninstall()

if __name__ == '__main__':
    main()
