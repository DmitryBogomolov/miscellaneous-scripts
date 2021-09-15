#!/usr/bin/env python3

from os import path
import subprocess

def convert2mp4(file_name: str, make_safe_name: bool=False) -> str:
    src_file = path.abspath(file_name)
    if not path.isfile(src_file):
        raise RuntimeError('file "{0}" does not exist'.format(src_file))

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

    if not do_convert(src_file, dst_file):
        raise RuntimeError('failed to convert')

    sync_attrs(src_file, dst_file)
    return dst_file

def do_convert(src_path: str, dst_path: str) -> bool:
    subprocess.run([
        'ffmpeg',
        '-i', src_path,
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict',
        '-2',
        '-q:a', '100',
        dst_path
    ])
    return path.isfile(dst_path)

def sync_attrs(src_path: str, dst_path: str) -> None:
    subprocess.run(['touch', '-r', src_path, dst_path])

def main():
    import argparse
    import sys
    parser = argparse.ArgumentParser(description='Converts to mp4')
    parser.add_argument('file_name', type=str)
    parser.add_argument('--safe-name', dest='use_safe_name', action='store_true', default=False)
    args = parser.parse_args(sys.argv[1:])
    convert2mp4(args.file_name, args.use_safe_name)

if __name__ == '__main__':
    main()
