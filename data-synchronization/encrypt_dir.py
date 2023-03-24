#!/usr/bin/env python3

from os import path
import util
import encrypt_file
import zip_dir

def encrypt_dir(dir_path: str, output_path: str, recipient: str) -> None:
    dir_path = path.abspath(dir_path)
    output_path = util.normalize_path_arg(output_path)
    output = output_path or encrypt_file.get_encrypted_name(dir_path)
    with util.make_tmp_dir(output) as tmp_path:
        tmp_archive_path = path.join(tmp_path, 'archive')
        zip_dir.zip_dir(dir_path, tmp_archive_path)
        encrypt_file.encrypt_file(tmp_archive_path, output, recipient)

def main() -> None:
    def setup_args(parser: util.ArgumentParser) -> None:
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
