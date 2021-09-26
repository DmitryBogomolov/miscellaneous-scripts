#!/bin/bash

if [[ "$#" -ne 4 ]]; then
    echo "smb_mount <smb_dir> <local_dir> <username> <password>"
    exit 2
fi

smb_dir="$1"
local_dir="$2"
username="$3"
password="$4"

uid="$(id -u)"
gid="$(id -g)"
# router host
host="$(route | grep default | awk '{ print $2 }')"
sudo mount -t cifs -o username="$username",password="$password",vers=1.0,uid="$uid",gid="$gid" "//$host$smb_dir" "$local_dir"
