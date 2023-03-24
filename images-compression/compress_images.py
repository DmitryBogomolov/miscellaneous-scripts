#!/usr/bin/env python3

from typing import Tuple, NamedTuple, Optional
from os import path
import os
import subprocess
import shutil

SUFFIX = '.CMPRSIMG'
MIN_QUALITY = 10
MAX_QUALITY = 100
MIN_MAX_SIZE = 400
MAX_MAX_SIZE = 8000

ImageSize = Tuple[int, int]

class ImageInfo(NamedTuple):
    file_path: str
    file_size: int
    image_size: ImageSize

    def __str__(self) -> str:
        kb_size = round(self.file_size / 1024)
        w, h = self.image_size
        return f'{self.file_path} ({kb_size}K, {w}x{h})'

    @classmethod
    def create(cls, file_path: str) -> 'ImageInfo':
        return ImageInfo(file_path, path.getsize(file_path), get_image_size(file_path))

def compress_image(
    file_path: str,
    out_dir: Optional[str] = None,
    quality: Optional[int] = None,
    max_size: Optional[int] = None,
    max_width: Optional[int] = None,
    max_height: Optional[int] = None,
    is_inplace: bool = False
) -> Tuple[ImageInfo, ImageInfo]:
    src_file = path.abspath(file_path)
    if not path.isfile(src_file):
        raise RuntimeError(f'"{src_file}" does not exist')
    src_info = ImageInfo.create(src_file)

    # Interim file is used to preserve original file (for inplace case) so that
    # its stats could then be copied.
    interim_file = get_interim_file_path(src_file)
    # There is an issue with `convert`.
    # Since 6.9.10-23 (approximately) version `-quality` outputs significantly larger (~6x) file.
    # This version is used in "focal" (u20) repositories.
    args = ['convert']
    new_size: Optional[ImageSize] = None
    if max_size is not None:
        new_size = restrict_max_size(src_info.image_size, max_size)
    elif max_width is not None:
        new_size = restrict_max_width(src_info.image_size, max_width)
    elif max_height is not None:
        new_size = restrict_max_height(src_info.image_size, max_height)
    if new_size is not None:
        width, height = new_size
        args.extend(['-resize', f'{width}x{height}>'])
    if quality is not None:
        args.extend(['-quality', str(quality) + '%'])
    args.extend([src_file, interim_file])

    subprocess.run(
        args,
        encoding='utf8', check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    shutil.copystat(src_file, interim_file)

    dst_file = prepare_dst_file(src_file, is_inplace, out_dir)
    # Using os.rename causes "Invalid cross-device link" error in docker.
    shutil.move(interim_file, dst_file)
    dst_info = ImageInfo.create(dst_file)
    return src_info, dst_info

def restrict_max_size(image_size: ImageSize, max_size: int) -> ImageSize:
    w_orig, h_orig = image_size
    if w_orig > h_orig:
        return restrict_max_width(image_size, max_size)
    else:
        return restrict_max_height(image_size, max_size)

def restrict_max_width(image_size: ImageSize, max_width: int) -> ImageSize:
    w_orig, h_orig = image_size
    w_curr = max_width
    h_curr = round(h_orig * w_curr / w_orig)
    return (w_curr, h_curr)

def restrict_max_height(image_size: ImageSize, max_height: int) -> ImageSize:
    w_orig, h_orig = image_size
    h_curr = max_height
    w_curr = round(w_orig * h_curr / h_orig)
    return (w_curr, h_curr)

def get_image_size(file_path: str) -> ImageSize:
    proc = subprocess.run(
        ['identify', '-format', r'%w %h', file_path],
        encoding='utf8', check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    w, h = map(int, proc.stdout.split())
    return (w, h)

def get_interim_file_path(file_path: str) -> str:
    name, ext = path.splitext(path.basename(file_path))
    return path.join(path.dirname(file_path), name + SUFFIX + ext)

def prepare_dst_file(file_path: str, is_inplace: bool, out_dir: Optional[str]) -> str:
    if is_inplace:
        return file_path
    dir_path = ''
    if out_dir:
        dir_path = path.abspath(out_dir)
    else:
        dir_path = path.join(path.dirname(file_path), SUFFIX)
    os.makedirs(dir_path, exist_ok=True)
    return path.join(dir_path, path.basename(file_path))

def main() -> None:
    import sys
    import argparse

    def check_quality_arg(val: str) -> int:
        try:
            quality = int(val)
            if quality < MIN_QUALITY or quality > MAX_QUALITY:
                raise ValueError(f'value is out of range [{MIN_QUALITY}, {MAX_QUALITY}]')
            return quality
        except Exception as err:
            raise argparse.ArgumentTypeError(err)

    def check_max_size_arg(val: str) -> int:
        try:
            max_size = int(val)
            if max_size < MIN_MAX_SIZE or MAX_MAX_SIZE > 8000:
                raise ValueError(f'value is out of range [{MIN_MAX_SIZE}, {MAX_MAX_SIZE}]')
            return max_size
        except Exception as err:
            raise argparse.ArgumentTypeError(err)

    parser = argparse.ArgumentParser(description='Compresses JPEG files')
    parser.add_argument(
        'targets',
        type=str, nargs='+',
        help='files to process'
    )
    parser.add_argument(
        '--quality',
        dest='quality', type=check_quality_arg,
        help=f'compression quality / [{MIN_QUALITY}, {MAX_QUALITY}]'
    )
    parser.add_argument(
        '--max-size',
        dest='max_size', type=check_max_size_arg,
        help=f'max width/height (which is greater) / [{MIN_MAX_SIZE}, {MAX_MAX_SIZE}]'
    )
    parser.add_argument(
        '--max-width',
        dest='max_width', type=check_max_size_arg,
        help=f'max width / [{MIN_MAX_SIZE}, {MAX_MAX_SIZE}]'
    )
    parser.add_argument(
        '--max-height',
        dest='max_height', type=check_max_size_arg,
        help=f'max height / [{MIN_MAX_SIZE}, {MAX_MAX_SIZE}]'
    )
    parser.add_argument(
        '--inplace',
        dest='is_inplace', action='store_true', default=False,
        help='replace file'
    )
    parser.add_argument(
        '--out-dir',
        dest='out_dir', type=str,
        help='output directory'
    )
    args = parser.parse_args(sys.argv[1:])

    for target in args.targets:
        try:
            src, dst = compress_image(
                file_path=target,
                out_dir=args.out_dir,
                quality=args.quality,
                max_size=args.max_size,
                max_width=args.max_width,
                max_height=args.max_height,
                is_inplace=args.is_inplace,
            )
            ratio = dst.file_size / src.file_size
            print(f'{src} -> {dst} // {ratio:.2f}')
        except Exception as err:
            print(err)

if __name__ == '__main__':
    main()
