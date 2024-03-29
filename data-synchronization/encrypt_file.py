#!/usr/bin/env python3

from os import path
import util

def get_encrypted_name(file_path: str) -> str:
    return file_path + '.pgp'

def encrypt_file(file_path: str, output_path: str, recipient: str) -> None:
    file_path = path.abspath(file_path)
    output_path = util.normalize_path_arg(output_path)
    util.check_file_exist(file_path)
    if not recipient:
        raise ValueError('recipient is not defined')
    output = output_path or get_encrypted_name(file_path)
    util.call_proc(['gpg', '--recipient', recipient, '--encrypt', '--output', output, file_path])

def main() -> None:
    def setup_args(parser: util.ArgumentParser) -> None:
        parser.add_argument('file', help='path to file')
        parser.add_argument('--output', help='path to encrypted file')
        parser.add_argument('--recipient', required=True, help='encryption recipient')
    args = util.parse_cmd_args(
        'Encrypts files.',
        setup_args
    )

    encrypt_file(args.file, args.output, args.recipient)

if __name__ == '__main__':
    main()
