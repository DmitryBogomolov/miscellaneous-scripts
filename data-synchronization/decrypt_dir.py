#!/usr/bin/env python3

from os import path
from tempfile import TemporaryDirectory
import util
import decrypt_file
import unzip_dir

def make_tmp_dir(output_path):
    return TemporaryDirectory(dir=path.dirname(output_path))

def decrypt_dir(file_path, output_path):
    file_path = path.abspath(file_path)
    output_path = util.normalize_path_arg(output_path)
    output = output_path or decrypt_file.get_decrypted_name(file_path)
    with make_tmp_dir(output) as tmp_path:
        tmp_archive_path = path.join(tmp_path, 'archive')
        decrypt_file.decrypt_file(file_path, tmp_archive_path)
        unzip_dir.unzip_dir(tmp_archive_path, output)

def main():
    def setup_args(parser):
        parser.add_argument('file', help='path to encrypted file')
        parser.add_argument('--output', help='path to directory')
    args = util.parse_cmd_args(
        'Decrypts directories.',
        setup_args
    )

    decrypt_dir(args.file, args.output)

if __name__ == '__main__':
    main()
