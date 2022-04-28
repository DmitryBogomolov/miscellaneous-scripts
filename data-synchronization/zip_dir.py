#!/usr/bin/env python3

from os import path
import shutil
import util

DEFAULT_FORMAT = 'zip'

def zip_dir(dir_path, output_path, archive_format = DEFAULT_FORMAT):
    dir_path = path.abspath(dir_path)
    output_path = output_path and path.abspath(output_path)
    base_name = output_path or dir_path
    shutil.make_archive(base_name, archive_format, dir_path)
    if output_path:
        shutil.move(base_name + '.' + archive_format, output_path)

def main():
    def setup_args(parser):
        parser.add_argument('dir', help='path to directory')
        parser.add_argument('--format', default=DEFAULT_FORMAT, help='archive format')
        parser.add_argument('--output', help='path to archive')
    args = util.parse_cmd_args(
        'Packs directory into archive.',
        setup_args
    )

    zip_dir(args.dir, args.output, args.format)

if __name__ == '__main__':
    main()
