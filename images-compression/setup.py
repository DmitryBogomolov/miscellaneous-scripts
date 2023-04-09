#!/usr/bin/env python3

import sys
import argparse
import os
from os import path
import stat
import shutil

BIN_DIR = path.expanduser('~/.local/bin')
SRC_DIR = path.dirname(path.abspath(__file__))
TARGET_PY = 'compress_images'
TARGET_SH = TARGET_PY + '_run'

def _install(target: str, ext: str) -> None:
    src_path = path.join(SRC_DIR, target + ext)
    dst_path = path.join(BIN_DIR, target)
    shutil.copy2(src_path, dst_path)
    os.chmod(dst_path, os.stat(dst_path).st_mode | stat.S_IEXEC)

def _uninstall(target: str) -> None:
    file_path = path.join(BIN_DIR, target)
    os.remove(file_path)

def install() -> None:
    _install(TARGET_PY, '.py')
    _install(TARGET_SH, '.sh')

def uninstall() -> None:
    _uninstall(TARGET_PY)
    _uninstall(TARGET_SH)

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
