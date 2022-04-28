#!/usr/bin/env python3

from os import path
import util

FILE_EXTENSION = '.pgp'

def is_encrypted_file(file_path):
    return file_path.endswith(FILE_EXTENSION)

def get_encrypted_name(name):
    return name + FILE_EXTENSION

def get_decrypted_name(name):
    return name[:-len(FILE_EXTENSION)]

def decrypt(file_path, output_path):
    args = ['gpg', '--decrypt']
    output = output_path or get_decrypted_name(file_path)
    args.extend(['--output', output, file_path])
    util.call_proc(args)

def encrypt(file_path, output_path, user_id):
    if not user_id:
        raise ValueError('encryption recipient is not provided')
    args = ['gpg', '--recipient', user_id, '--encrypt']
    output = output_path or get_encrypted_name(file_path)
    args.extend(['--output', output, file_path])
    util.call_proc(args)

def encrypt_file(file_path, output_path, user_id):
    full_file_path = path.abspath(file_path)
    full_output_path = output_path and path.abspath(output_path)
    util.check_file_exist(full_file_path)
    if is_encrypted_file(full_file_path):
        decrypt(full_file_path, full_output_path)
    else:
        encrypt(full_file_path, full_output_path, user_id)

def main():
    def setup_args(parser):
        parser.add_argument('file', help='path to file')
        parser.add_argument('--output', help='path to output')
        parser.add_argument('--user', help='user for encryption')
    args = util.parse_cmd_args(
        'Encrypts and decrypts files.',
        setup_args
    )

    encrypt_file(args.file, args.output, args.user)

if __name__ == '__main__':
    main()
