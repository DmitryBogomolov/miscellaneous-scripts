#!/usr/bin/env python3

from os import path
import util

def get_file_path(dir_path: str) -> str:
    return dir_path + '.zip'

def zip_dir(dir_path: str, output_path: str) -> None:
    dir_path = path.abspath(dir_path)
    output_path = util.normalize_path_arg(output_path) or get_file_path(dir_path)
    util.check_dir_exist(dir_path)
    util.call_proc(['zip', '-Ar', output_path, '.'], cwd=dir_path)

def main() -> None:
    def setup_args(parser: util.ArgumentParser) -> None:
        parser.add_argument('dir', help='path to directory')
        parser.add_argument('--output', help='path to archive')
    args = util.parse_cmd_args(
        'Packs directory into archive.',
        setup_args
    )

    zip_dir(args.dir, args.output)

if __name__ == '__main__':
    main()
