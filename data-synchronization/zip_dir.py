#!/usr/bin/env python3

from os import path
import util

def zip_dir(dir_path, output_path):
    dir_path = path.abspath(dir_path)
    output_path = util.normalize_path_arg(output_path) or dir_path
    util.call_proc(['zip', '-Ar', output_path, '.'], cwd=dir_path)

def main():
    def setup_args(parser):
        parser.add_argument('dir', help='path to directory')
        parser.add_argument('--output', help='path to archive')
    args = util.parse_cmd_args(
        'Packs directory into archive.',
        setup_args
    )

    zip_dir(args.dir, args.output)

if __name__ == '__main__':
    main()
