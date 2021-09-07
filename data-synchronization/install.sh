#!/bin/bash

BIN_DIR="$HOME/.local/bin"

install() {
    local src_path="$1"
    local dst_path="$BIN_DIR/${src_path%%.*}"
    echo "$src_path -> $dst_path"
    cp "$src_path" "$dst_path"
    touch -r "$src_path" "$dst_path"
    chmod +x "$dst_path"
}

install sync_folders.sh
