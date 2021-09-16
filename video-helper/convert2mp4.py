#!/usr/bin/env python3

from os import path
import shutil
import subprocess

def convert2mp4(file_name, make_safe_name=False):
    src_file = path.abspath(file_name)
    if not path.isfile(src_file):
        raise RuntimeError('file "{}" does not exist'.format(src_file))

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
    except:
        raise RuntimeError('failed to convert "{}"'.format(src_file))

    shutil.copystat(src_file, dst_file)
    return dst_file

def call_ffmpeg(src_path, dst_path):
    args = [
        'ffmpeg',
        '-i', src_path,
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict',
        '-2',
        '-q:a', '100',
        dst_path
    ]
    subprocess.run(args, encoding='utf8', check=True)

def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Converts to mp4')
    parser.add_argument('file_name', type=str)
    parser.add_argument('--safe-name', dest='make_safe_name', action='store_true', default=False)
    args = parser.parse_args(sys.argv[1:])

    convert2mp4(args.file_name, args.make_safe_name)

if __name__ == '__main__':
    main()
