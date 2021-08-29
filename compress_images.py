#!/usr/bin/env python3

def compress_image(file_path):
    pass

def main():
    import sys
    import argparse
    parser = argparse.ArgumentParser(description='Compresses images')
    parser.add_argument('targets', type=str, nargs='+')
    args = parser.parse_args(sys.argv[1:])
    print(args.targets)

if __name__ == '__main__':
    main()
