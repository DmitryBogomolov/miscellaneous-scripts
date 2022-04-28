#!/usr/bin/env python3

from os import path
import shutil
import util

DEFAULT_FORMAT = 'zip'

def zip_directory(dir_path, archive_path, archive_format):
    base_name = archive_path or dir_path
    shutil.make_archive(base_name, archive_format, dir_path)
    if archive_path:
        shutil.move(base_name + '.' + archive_format, archive_path)

def unzip_archive(archive_path, dir_path, archive_format):
    dir_name = dir_path or path.splitext(archive_path)[0]
    if dir_name == archive_path:
        dir_name += '_'
    shutil.unpack_archive(archive_path, dir_name, archive_format)

def zip_dir(target_path, output_path, archive_format = DEFAULT_FORMAT):
    full_target_path = path.abspath(target_path)
    full_output_path = output_path and path.abspath(output_path)
    if path.isfile(full_target_path):
        unzip_archive(full_target_path, full_output_path, archive_format)
    else:
        zip_directory(full_target_path, full_output_path, archive_format)

def main():
    def setup_args(parser):
        parser.add_argument('target', help='path to directory or archive')
        parser.add_argument('--format', default=DEFAULT_FORMAT, help='archive format')
        parser.add_argument('--output', help='path to archive or directory')
    args = util.parse_cmd_args(
        'Packs directory into archive or unpacks archive into directory.',
        setup_args
    )

    zip_dir(args.target, args.output, args.format)

if __name__ == '__main__':
    main()
