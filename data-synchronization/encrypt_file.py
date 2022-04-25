#!/usr/bin/env python3

import os.path as path
import util

FILE_EXTENSION = '.pgp'

def decrypt(file_path, output_path, is_dry_run):
    args = ['gpg', '--decrypt']
    if is_dry_run:
        args.append('--dry-run')
    # use output or strip encryption extension
    output = output_path or file_path[:-len(FILE_EXTENSION)]
    args.extend(['--output', output, file_path])
    util.call_proc(args)

def encrypt(file_path, output_path, user_id, is_dry_run):
    if not user_id:
        raise RuntimeError('encryption recipient is not provided')
    args = ['gpg', '--recipient', user_id, '--encrypt']
    if is_dry_run:
        args.append('--dry-run')
    output = output_path or (file_path + FILE_EXTENSION)
    args.extend(['--output', output, file_path])
    util.call_proc(args)

def encrypt_file(file_path, output_path, user_id, dry_run):
    full_file_path = path.abspath(file_path)
    full_output_path = output_path and path.abspath(output_path)
    is_dry_run = util.is_dry_run(dry_run)
    util.check_file_exist(full_file_path)
    if full_file_path.endswith(FILE_EXTENSION):
        decrypt(full_file_path, full_output_path, is_dry_run)
    else:
        encrypt(full_file_path, full_output_path, user_id, is_dry_run)

def main():
    def setup_args(parser):
        parser.add_argument('file', help='path to file')
        parser.add_argument('--output', help='path to output')
        parser.add_argument('--user', help='user for encryption')
    args = util.parse_cmd_args(
        'Encrypts and decrypts files.',
        setup_args,
        add_dry_run=True
    )

    encrypt_file(args.file, args.output, args.user, args.dry_run)

if __name__ == '__main__':
    main()
