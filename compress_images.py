#!/usr/bin/env python3

from os import path
import os
import subprocess
import shutil

DEFAULT_QUALITY = 20
SUFFIX = '.CMPRSIMG'

class ImageInfo(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_size = path.getsize(file_path)
        w, h = get_image_size(file_path)
        self.image_size = [w, h]

    def __str__(self):
        return '{} ({}K, {}x{})'.format(
            self.file_path, round(self.file_size / 1024), self.image_size[0], self.image_size[1]
        )

def compress_image(file_path, quality, is_inplace=False, out_dir=None):
    src_file = path.abspath(file_path)
    if not path.isfile(src_file):
        raise RuntimeError('"{0}" does not exist'.format(src_file))
    interim_file = get_interim_file_path(src_file)

    try:
        subprocess.run(
            ['convert', '-quality', str(quality) + '%', src_file, interim_file],
            encoding='utf8', check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        shutil.copystat(src_file, interim_file)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('failed to compress "{}": {}'.format(src_file, str(e)))

    dst_file = prepare_dst_file(src_file, is_inplace, out_dir)
    os.rename(interim_file, dst_file)
    return ImageInfo(src_file), ImageInfo(dst_file)

def get_image_size(file_path):
    try:
        proc = subprocess.run(
            ['identify', '-format', r'%w %h', file_path],
            encoding='utf8', check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        w, h = map(int, proc.stdout.split())
        return [w, h]
    except subprocess.CalledProcessError as e:
        raise RuntimeError(str(e))


def get_interim_file_path(file_path):
    name, ext = path.splitext(path.basename(file_path))
    return path.join(path.dirname(file_path), name + SUFFIX + ext)

def prepare_dst_file(file_path, is_inplace, out_dir):
    if is_inplace:
        return file_path
    dir_path = path.abspath(out_dir) if out_dir else path.join(path.dirname(file_path), SUFFIX)
    os.makedirs(dir_path, exist_ok=True)
    return path.join(dir_path, path.basename(file_path))

def main():
    import sys
    import argparse

    def check_quality_arg(val):
        try:
            quality = int(val)
            if quality < 10 or quality > 99:
                raise ValueError('value is out of range')
        except Exception as e:
            raise argparse.ArgumentTypeError(e)

    parser = argparse.ArgumentParser(description='Compresses images')
    parser.add_argument('targets', type=str, nargs='+')
    parser.add_argument('--quality', dest='quality', type=check_quality_arg, default=DEFAULT_QUALITY)
    parser.add_argument('--inplace', dest='is_inplace', action='store_true', default=False)
    parser.add_argument('--out-dir', dest='out_dir', type=str)
    args = parser.parse_args(sys.argv[1:])
    for target in args.targets:
        try:
            src, dst = compress_image(target, args.quality, args.is_inplace, args.out_dir)
            print('{} -> {} ## {}'.format(src, dst, format(src.file_size / dst.file_size, '.2f')))
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
