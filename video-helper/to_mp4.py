#!/usr/bin/env python3

import os
from os import path
import shutil
import subprocess

def to_mp4(file_name: str, make_safe_name: bool = False) -> str:
    src_file = path.abspath(file_name)
    if not path.isfile(src_file):
        raise RuntimeError(f'file "{src_file}" does not exist')

    src_dir = path.dirname(src_file)
    src_name = path.basename(src_file)
    name, _ = path.splitext(src_name)
    dst_dir = src_dir
    dst_name = name + '.mp4'
    if make_safe_name:
        dst_name = dst_name.replace(' ', '_')
    dst_file = path.join(dst_dir, dst_name)

    if path.isfile(dst_file):
        return dst_file

    try:
        call_ffmpeg(src_file, dst_file)
    except subprocess.SubprocessError as err:
        raise RuntimeError(f'failed to convert "{src_file}"') from err

    shutil.copystat(src_file, dst_file)
    return dst_file

def call_ffmpeg(src_path: str, dst_path: str) -> None:
    args = [
        'ffmpeg',
        '-i', src_path,
        '-c:v', 'libx264',
        #'-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict',
        '-2',
        '-q:a', '100',
        dst_path
    ]
    try:
        subprocess.run(args, encoding='utf8', check=True)
    except:
        if path.isfile(dst_path):
            os.remove(dst_path)
        raise

def main() -> None:
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Converts file to mp4')
    parser.add_argument(
        'file_name', type=str,
        help='file to convert'
    )
    parser.add_argument(
        '--safe-name', dest='make_safe_name', action='store_true', default=False,
        help='replace spaces in file name'
    )
    args = parser.parse_args(sys.argv[1:])

    to_mp4(args.file_name, args.make_safe_name)

if __name__ == '__main__':
    main()
