#!/usr/bin/env python3

from os import path
import shutil
import util

DEFAULT_FORMAT = 'zip'

def unzip_dir(archive_path, output_path, archive_format = DEFAULT_FORMAT):
    archive_path = path.abspath(archive_path)
    output_path = util.normalize_path_arg(output_path)
    dir_name = output_path or path.splitext(archive_path)[0]
    if dir_name == archive_path:
        dir_name += '_'
    shutil.unpack_archive(archive_path, dir_name, archive_format)

def main():
    def setup_args(parser):
        parser.add_argument('archive', help='path to archive')
        parser.add_argument('--format', default=DEFAULT_FORMAT, help='archive format')
        parser.add_argument('--output', help='path to directory')
    args = util.parse_cmd_args(
        'Unpacks directory from archive.',
        setup_args
    )

    unzip_dir(args.archive, args.output, args.format)

if __name__ == '__main__':
    main()
