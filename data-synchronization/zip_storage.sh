#!/bin/bash

if [[ -z "$SYNC_MISK_DISK" ]]; then
    echo "SYNC_MISK_DISK is not set"
    exit 1
fi

disk="/media/$USER/$SYNC_MISK_DISK"
# config format: "src_dir:dst_dir:file_name_without_ext"
config="$disk/.zip_storage"

if [[ ! -f "$config" ]]; then
    echo "$config does not exist"
    exit 1
fi

IFS=: read -r src_dir dst_dir file_name <<< "$(cat $config)"
src_dir="$disk/$src_dir"
dst_dir="$disk/$dst_dir"
file_name="$file_name.zip"

cd "$src_dir"
zip -re "$file_name" .
mv "$file_name" "$dst_dir"
