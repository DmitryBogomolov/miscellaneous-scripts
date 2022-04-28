#!/usr/bin/env python3

from os import path
from tempfile import TemporaryDirectory
import util
import encrypt_file
import zip_dir

def make_tmp_dir(output_path):
    return TemporaryDirectory(dir=path.dirname(output_path))

def encrypt_dir(dir_path, output_path, recipient):
    dir_path = path.abspath(dir_path)
    output_path = output_path and path.abspath(output_path)
    output = output_path or encrypt_file.get_encrypted_name(dir_path)
    with make_tmp_dir(output) as tmp_path:
        tmp_archive_path = path.join(tmp_path, 'archive')
        zip_dir.zip_dir(dir_path, tmp_archive_path)
        encrypt_file.encrypt_file(tmp_archive_path, output, recipient)


def main():
    def setup_args(parser):
        parser.add_argument('dir', help='path to directory')
        parser.add_argument('--output', help='path to encrypted file')
        parser.add_argument('--recipient', help='encryption recipient')
    args = util.parse_cmd_args(
        'Encrypts directories.',
        setup_args
    )

    encrypt_dir(args.dir, args.output, args.recipient)

if __name__ == '__main__':
    main()
