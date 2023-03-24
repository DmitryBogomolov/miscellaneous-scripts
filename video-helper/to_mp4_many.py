#!/usr/bin/env python3

from typing import List
import multiprocessing
from to_mp4 import to_mp4

DEFAULT_PROCESSES_COUNT = 8

def to_mp4_many(file_names: List[str], processes_count: int = DEFAULT_PROCESSES_COUNT) -> List[str]:
    with multiprocessing.Pool(processes_count) as pool:
        mp4_file_names = pool.map(to_mp4, file_names)
    return mp4_file_names

def main() -> None:
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Converts files to mp4')
    parser.add_argument(
        'file_names', type=str, nargs='+',
        help='files to convert'
    )
    parser.add_argument(
        '--processes-count', dest='processes_count', default=DEFAULT_PROCESSES_COUNT, type=int,
        help='count of parallel processes'
    )
    args = parser.parse_args(sys.argv[1:])

    to_mp4_many(args.file_names, args.processes_count)

if __name__ == '__main__':
    main()
