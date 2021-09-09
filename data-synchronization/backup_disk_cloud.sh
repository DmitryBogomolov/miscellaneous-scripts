#!/bin/bash

if [[ "$#" -ne 2 ]]; then
    echo "backup_disk_cloud disk_name bucket_name"
    exit 2
fi

disk="/media/$USER/$1"
bucket="s3://$2"
list_file="$disk/.backup_disk_cloud"

if [[ ! -d "$disk" ]]; then
    echo "directory '$disk' does not exist"
    exit 1
fi

if [[ ! -f "$list_file" ]]; then
    echo "file '$list_file' does not exist"
    exit 1
fi

dirs=()
while read item; do
    if [[ ! -z "$item" ]]; then
        dirs=("${dirs[@]}" "$item")
    fi
done < "$list_file"

do_sync () {
    local src_dir="$disk/$1/"
    local dst_dir="$bucket/$1/"
    echo "### '$src_dir' --> '$dst_dir'"
    options=(--delete)
    if [[ ! -z "$SYNC_DRY_RUN" ]]; then
        options=(${options[@]} --dryrun)
    fi
    aws s3 sync "${options[@]}" "$src_dir" "$dst_dir"
}

begin_time="$SECONDS"
for dir in "${dirs[@]}"; do
    do_sync "$dir"
done
end_time="$SECONDS"
duration="$((end_time - begin_time))"
echo "Time: $duration"
