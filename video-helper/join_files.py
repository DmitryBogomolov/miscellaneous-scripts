#!/usr/bin/env python3

from typing import List
import os
from os import path
import shutil
import subprocess

def join_files(file_names: List[str], out_file: str) -> None:
    out_file_path = path.abspath(out_file)
    list_file_path = out_file_path + '.list'
    with open(list_file_path, 'w', encoding='utf8') as file_buffer:
        for file_name in file_names:
            list_file_entry = f'file \'{path.abspath(file_name)}\'\n'
            file_buffer.write(list_file_entry)

    try:
        call_ffmpeg(list_file_path, out_file_path)
    except subprocess.SubprocessError as err:
        raise RuntimeError('failed to join files') from err
    finally:
        os.remove(list_file_path)

    shutil.copystat(path.abspath(file_names[0]), out_file_path)

def call_ffmpeg(list_file_path: str, out_file_path: str) -> None:
    args = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', list_file_path,
        '-c', 'copy',
        out_file_path
    ]
    try:
        subprocess.run(args, encoding='utf8', check=True)
    except:
        if path.isfile(out_file_path):
            os.remove(out_file_path)
        raise

def main() -> None:
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Joins files')
    parser.add_argument(
        'file_names', type=str, nargs='+',
        help='files to join'
    )
    parser.add_argument(
        '--out-file', type=str, required=True, dest='out_file',
        help='joined file'
    )
    args = parser.parse_args(sys.argv[1:])

    join_files(args.file_names, args.out_file)

if __name__ == '__main__':
    main()
