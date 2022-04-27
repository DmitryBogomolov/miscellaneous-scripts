#!/usr/bin/env python3

from os import path
from tempfile import TemporaryDirectory
import util
import encrypt_file
import zip_dir

def make_tmp_dir(output_path):
    return TemporaryDirectory(dir=path.dirname(output_path))

def decrypt(file_path, output_path):
    output = output_path or encrypt_file.get_decrypted_name(file_path)
    with make_tmp_dir(output) as tmp_path:
        tmp_archive_path = path.join(tmp_path, 'archive')
        encrypt_file.encrypt_file(file_path, tmp_archive_path, None)
        zip_dir.zip_dir(tmp_archive_path, output)

def encrypt(dir_path, output_path, user_id):
    output = output_path or encrypt_file.get_encrypted_name(dir_path)
    with make_tmp_dir(output) as tmp_path:
        tmp_archive_path = path.join(tmp_path, 'archive')
        zip_dir.zip_dir(dir_path, tmp_archive_path)
        encrypt_file.encrypt_file(tmp_archive_path, output, user_id)

def encrypt_dir(target_path, output_path, user_id):
    full_target_path = path.abspath(target_path)
    full_output_path = output_path and path.abspath(output_path)
    if encrypt_file.is_encrypted_file(full_target_path):
        util.check_file_exist(full_target_path)
        decrypt(full_target_path, full_output_path)
    else:
        util.check_dir_exist(full_target_path)
        encrypt(full_target_path, full_output_path, user_id)

def main():
    def setup_args(parser):
        parser.add_argument('path', help='path to file or directory')
        parser.add_argument('--output', help='path to output')
        parser.add_argument('--user', help='user for encryption')
    args = util.parse_cmd_args(
        'Encrypts and decrypts directories.',
        setup_args
    )

    encrypt_dir(args.path, args.output, args.user)

if __name__ == '__main__':
    main()
