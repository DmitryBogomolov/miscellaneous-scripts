#!/bin/bash

if [[ "$#" -ne 2 ]]; then
    echo "zip_dir /path/to/dir /path/to/archive.zip"
    exit 2
fi

src_dir="$1"
dst_dir=$(dirname "$2")
file_name=$(basename "$2")

check_dir() {
    if [[ ! -d "$1" ]]; then
        echo "directory '$1' does not exist"
        exit 1
    fi
}
check_dir "$src_dir"
check_dir "$dst_dir"

cd "$src_dir"
zip -re "$file_name" .
mv "$file_name" "$dst_dir"
