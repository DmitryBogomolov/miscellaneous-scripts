#!/usr/bin/env python3

from os import path
import util

def get_dir_path(archive_path: str) -> str:
    dir_path, ext = path.splitext(archive_path)
    if not ext:
        dir_path += '_zip'
    return dir_path

def unzip_dir(archive_path: str, output_path: str) -> None:
    archive_path = path.abspath(archive_path)
    output_path = util.normalize_path_arg(output_path) or get_dir_path(archive_path)
    util.check_file_exist(archive_path)
    util.call_proc(['unzip', '-d', output_path, archive_path])

def main() -> None:
    def setup_args(parser: util.ArgumentParser) -> None:
        parser.add_argument('archive', help='path to archive')
        parser.add_argument('--output', help='path to directory')
    args = util.parse_cmd_args(
        'Unpacks directory from archive.',
        setup_args
    )

    unzip_dir(args.archive, args.output)

if __name__ == '__main__':
    main()
