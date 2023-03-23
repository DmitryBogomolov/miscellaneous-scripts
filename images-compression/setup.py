#!/usr/bin/env python3

import sys
import argparse
import os
from os import path
import stat
import shutil

BIN_DIR = path.expanduser('~/.local/bin')
TARGET = 'compress_images'

def install() -> None:
    src_path = path.join(path.dirname(path.abspath(__file__)), TARGET + '.py')
    dst_path = path.join(BIN_DIR, TARGET)
    shutil.copy2(src_path, dst_path)
    os.chmod(dst_path, os.stat(dst_path).st_mode | stat.S_IEXEC)

def uninstall() -> None:
    file_path = path.join(BIN_DIR, TARGET)
    os.remove(file_path)

def main() -> None:
    parser = argparse.ArgumentParser(description='Manages script')
    parser.add_argument('mode', choices=['on', 'off'], help='Add or remove script')
    args = parser.parse_args(sys.argv[1:])

    if args.mode == 'on':
        install()
    if args.mode == 'off':
        uninstall()

if __name__ == '__main__':
    main()
