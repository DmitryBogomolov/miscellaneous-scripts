#!/usr/bin/env python3

def convert_and_join(file_names, out_file):
    pass

def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Converts files to .mp4 and joins them')
    parser.add_argument('file_names', type=str, nargs='+', help='files to join')
    parser.add_argument('--out-file', type=str, required=True, dest='out_file', help='joined file')
    args = parser.parse_args(sys.argv[1:])

    convert_and_join(args.file_names, args.out_file)

if __name__ == '__main__':
    main()
