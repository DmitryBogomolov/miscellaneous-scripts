#!/usr/bin/env python3

from os import path
import os
import subprocess
import shutil

DEFAULT_QUQLITY = 20
SUFFIX = '.CMPRSIMG'

def compress_image(file_path, quality, is_inplace=False, out_dir=None):
    src_file = path.abspath(file_path)
    if not path.isfile(src_file):
        raise RuntimeError('"{0}" does not exist'.format(src_file))
    interim_file = get_interim_file_path(src_file)

    try:
        subprocess.run(
            ['convert', '-quality', str(quality) + '%', src_file, interim_file],
            capture_output=True, text=True, check=True
        )
        shutil.copystat(src_file, interim_file)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('failed to compress "{0}": {1}'.format(src_file. str(e)))

    dst_file = ''
    if is_inplace:
        dst_file = src_file
    elif out_dir:
        dst_file = prepare_dst_dir(path.abspath(out_dir), src_file)
    else:
        dst_file = prepare_dst_dir(path.join(path.dirname(src_file), SUFFIX), src_file)

    print('TEST', interim_file, dst_file)
    os.rename(interim_file, dst_file)

def get_image_data(file_path):
    try:
        proc = subprocess.run(
            ['identify', '-format', r'%B %w %h %Q', file_path],
            capture_output=True, text=True, check=True
        )
        size_str, w_str, h_str, quality_str = proc.stdout.split()
        return [int(size_str), int(w_str), int(h_str), int(quality_str)]
    except subprocess.CalledProcessError as e:
        raise RuntimeError(str(e))


def get_interim_file_path(file_path):
    name, ext = path.splitext(path.basename(file_path))
    return path.join(path.dirname(file_path), name + SUFFIX + ext)

def prepare_dst_dir(dir_path, file_path):
    os.makedirs(dir_path, exist_ok=True)
    return path.join(dir_path, path.basename(file_path))

def main():
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Compresses images')
    parser.add_argument('targets', type=str, nargs='+')
    parser.add_argument('--quality', type=int, default=DEFAULT_QUQLITY)
    parser.add_argument('--inplace', dest='is_inplace', action='store_true', default=False)
    parser.add_argument('--out-dir', dest='out_dir', type=str)
    args = parser.parse_args(sys.argv[1:])
    for target in args.targets:
        compress_image(target, args.quality, args.is_inplace, args.out_dir)

if __name__ == '__main__':
    main()
