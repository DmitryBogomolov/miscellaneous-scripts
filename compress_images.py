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
    tmp_file = get_working_name(src_file)
    proc = subprocess.run(['convert', '-quality', str(quality) + '%', src_file, tmp_file])
    if proc.returncode != 0:
        if path.isfile(tmp_file):
            os.remove(tmp_file)
        raise RuntimeError('failed to compress "{0}"'.format(src_file))
    shutil.copystat(src_file, tmp_file)
    dst_file = ''
    if is_inplace:
        dst_file = src_file
    elif out_dir:
        dst_file = prepare_dst_dir(path.abspath(out_dir), src_file)
    else:
        dst_file = prepare_dst_dir(path.join(path.dirname(src_file), SUFFIX), src_file)
    print('TEST', tmp_file, dst_file)
    os.rename(tmp_file, dst_file)

def get_working_name(file_path):
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
