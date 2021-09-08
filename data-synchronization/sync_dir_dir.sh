#!/bin/bash

if [[ "$#" -ne 2 ]]; then
    echo "sync_dir_dir /path/to/src /path/to/dst"
    exit 2
fi

src_dir="$1"
dst_dir="$2"

check_dir() {
    if [[ ! -d "$1" ]]; then
        echo "directory '$1' does not exist"
        exit 1
    fi
}

check_dir "$src_dir"
check_dir "$dst_dir"

options=(--archive --delete --compress --progress -v -h)
if [[ ! -z "$SYNC_DRY_RUN" ]]; then
    options=(${options[@]} --dry-run)
fi

rsync "${options[@]}" "$src_dir" "$dst_dir"
