#!/usr/bin/env python3

import os.path as path
import util

def decrypt(file_path, is_dry_run):
    args = ['gpg', '--decrypt']
    if is_dry_run:
        args.append('--dry-run')
    args.extend(['--output', file_path.rstrip('.pgp'), file_path])
    util.call_proc(args)

def encrypt(file_path, user_id, is_dry_run):
    if not user_id:
        raise RuntimeError('recipient is not provided')
    args = ['gpg', '--recipient', user_id, '--encrypt']
    if is_dry_run:
        args.append('--dry-run')
    args.extend(['--output', file_path + '.pgp', file_path])
    util.call_proc(args)

def encrypt_file(file_path, user_id, dry_run):
    full_path = path.abspath(file_path)
    is_dry_run = util.is_dry_run(dry_run)
    util.check_file_exist(full_path)
    if full_path.endswith('.pgp'):
        decrypt(full_path, is_dry_run)
    else:
        encrypt(full_path, user_id, is_dry_run)

def main():
    def setup_args(parser):
        parser.add_argument('file', help='path to file')
        parser.add_argument('--user', help='user for encryption')
    args = util.parse_cmd_args(
        'Encrypts and decrypts files.',
        setup_args,
        add_dry_run=True
    )

    encrypt_file(args.file, args.user, args.dry_run)

if __name__ == '__main__':
    main()
