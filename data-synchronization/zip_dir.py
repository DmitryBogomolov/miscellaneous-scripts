#!/usb/bin/env python3

import sys
import argparse
import os.path as path
import shutil

def zip_directory(dir_path, archive_path):
    archive_format = 'zip'
    archive_name = dir_path
    if archive_path:
        archive_name, archive_format = path.splitext(archive_path)
        archive_format = archive_format[1:]
    shutil.make_archive(archive_name, archive_format, dir_path)

def unzip_archive(archive_path, dir_path):
    dir_name = path.splitext(archive_path)[0]
    if dir_path:
        dir_name = dir_path
    shutil.unpack_archive(archive_path, dir_name)

def main():
    parser = argparse.ArgumentParser(
        description='Packs directory into archive or unpacks archive into directory.'
    )
    parser.add_argument('target', help='path to directory or archive')
    parser.add_argument('--output', help='path to archive or directory')
    args = parser.parse_args(sys.argv[1:])

    target = path.abspath(args.target)
    output = path.abspath(args.output) if args.output is not None else None
    if path.isdir(target):
        zip_directory(target, output)
    elif path.isfile(target) and path.splitext(target)[1] == '.zip':
        unzip_archive(target, output)
    else:
        raise RuntimeError('{} is neigher directory nor zip file'.format(target))

if __name__ == '__main__':
    main()
