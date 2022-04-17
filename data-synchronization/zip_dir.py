#!/usb/bin/env python3

import os.path as path
import shutil
import util

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

def zip_dir(target_path, output_path):
    target = path.abspath(target_path)
    output = path.abspath(output_path) if output_path is not None else None
    if path.isdir(target):
        zip_directory(target, output)
    elif path.isfile(target):
        unzip_archive(target, output)
    else:
        raise RuntimeError('"{}" is neigher directory nor archive file'.format(target))

def main():
    def setup_args(parser):
        parser.add_argument('target', help='path to directory or archive')
        parser.add_argument('--output', help='path to archive or directory')
    args = util.parse_cmd_args(
        'Packs directory into archive or unpacks archive into directory.',
        setup_args
    )

    zip_dir(args.target, args.output)

if __name__ == '__main__':
    main()
