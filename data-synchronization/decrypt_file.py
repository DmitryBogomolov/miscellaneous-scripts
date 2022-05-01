#!/usr/bin/env python3

from os import path
import util

def get_decrypted_name(file_path):
    name_part, ext = path.splitext(file_path)
    if not ext:
        name_part += '_pgp'
    return name_part

def decrypt_file(file_path, output_path):
    file_path = path.abspath(file_path)
    output_path = util.normalize_path_arg(output_path)
    util.check_file_exist(file_path)
    output = output_path or get_decrypted_name(file_path)
    util.call_proc(['gpg', '--decrypt', '--output', output, file_path])

def main():
    def setup_args(parser):
        parser.add_argument('file', help='path to encrypted file')
        parser.add_argument('--output', help='path to file')
    args = util.parse_cmd_args(
        'Decrypts files.',
        setup_args
    )

    decrypt_file(args.file, args.output)

if __name__ == '__main__':
    main()
