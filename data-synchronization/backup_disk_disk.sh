#!/bin/bash

if [[ "$#" -ne 2 ]]; then
    echo "backup_disk_disk src_disk_name dst_disk_name"
    exit 2
fi

src_disk="/media/$USER/$1"
dst_disk="/media/$USER/$2"
list_file="$src_disk/.backup_disk_disk"

if [[ ! -d "$src_disk" ]]; then
    echo "directory '$src_disk' does not exist"
    exit 1
fi

if [[ ! -d "$dst_disk" ]]; then
    echo "directory '$dst_disk' does not exist"
    exit 1
fi

if [[ ! -f "$list_file" ]]; then
    echo "file '$list_file' does not exist"
    exit 1
fi

dirs=()
while read item; do
    dirs=("${dirs[@]}" "$item")
done < "$list_file"

do_sync () {
    local src_dir="$1"
    local dst_dir="$2"
    local folder_name="$3"
    local src="$src_dir/$folder_name/"
    local dst="$dst_dir/$folder_name/"
    echo "### '$src' --> '$dst'"
    sync_dir_dir "$src" "$dst"
    echo ""
}

begin_time="$SECONDS"
for dir in "${dirs[@]}"; do
    do_sync "$src_disk" "$dst_disk" "$dir"
done
end_time="$SECONDS"
duration="$((end_time - begin_time))"
echo "Time: $duration"
