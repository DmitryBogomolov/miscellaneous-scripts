#!/usr/bin/env python3

from os import path
import os
import subprocess
import shutil

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

def compress_image(file_path, quality, max_size, is_inplace, out_dir):
    src_file = path.abspath(file_path)
    if not path.isfile(src_file):
        raise RuntimeError('"{0}" does not exist'.format(src_file))
    src_info = ImageInfo(src_file)

    interim_file = get_interim_file_path(src_file)
    args = ['convert']
    if max_size is not None:
        args.extend(['-resize', get_resize_param(src_info.image_size, max_size)])
    if quality is not None:
        args.extend(['-quality', str(quality) + '%'])
    args.extend([src_file, interim_file])

    subprocess.run(
        args,
        encoding='utf8', check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    shutil.copystat(src_file, interim_file)

    dst_file = prepare_dst_file(src_file, is_inplace, out_dir)
    os.rename(interim_file, dst_file)
    dst_info = ImageInfo(dst_file)
    return src_info, dst_info

def get_resize_param(image_size, max_size):
    w_orig, h_orig = image_size
    w_curr, h_curr = w_orig, h_orig
    if w_orig > h_orig:
        w_curr = max_size
        h_curr = round(h_orig * w_curr / w_orig)
    else:
        h_curr = max_size
        w_curr = round(w_orig * h_curr / h_orig)
    return str(w_curr) + 'x' + str(h_curr) + '>'

def get_image_size(file_path):
    proc = subprocess.run(
        ['identify', '-format', r'%w %h', file_path],
        encoding='utf8', check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    w, h = map(int, proc.stdout.split())
    return [w, h]

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
            return quality
        except Exception as e:
            raise argparse.ArgumentTypeError(e)

    def check_max_size_arg(val):
        try:
            max_size = int(val)
            if max_size < 400 or max_size > 8000:
                raise ValueError('value is out of range')
            return max_size
        except Exception as e:
            raise argparse.ArgumentTypeError(e)

    parser = argparse.ArgumentParser(description='Compresses images')
    parser.add_argument('targets', type=str, nargs='+')
    parser.add_argument('--quality', dest='quality', type=check_quality_arg)
    parser.add_argument('--max-size', dest='max_size', type=check_max_size_arg)
    parser.add_argument('--inplace', dest='is_inplace', action='store_true', default=False)
    parser.add_argument('--out-dir', dest='out_dir', type=str)
    args = parser.parse_args(sys.argv[1:])
    for target in args.targets:
        try:
            src, dst = compress_image(
                target,
                args.quality, args.max_size, args.is_inplace, args.out_dir
            )
            print('{} -> {} // {}'.format(
                src, dst, format(dst.file_size / src.file_size * 100, '.2f') + '%'
            ))
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
