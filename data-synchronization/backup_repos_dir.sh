#!/bin/bash

if [[ "$#" -ne 1 ]]; then
    echo "backup_repos_dir repos_dir"
    exit 2
fi

repos_dir="$(realpath $1)"

if [[ ! -d "$repos_dir" ]]; then
    echo "directory '$repos_dir' does not exist"
    exit 1
fi

backup_repo() {
    repo_dir="$1"
    cd "$repo_dir"
    remote_url="$(git config remote.origin.url)"
    echo "### '$remote_url' --> '$repo_dir'"
    options=(--prune --verbose --force --ff-only --stat)
    if [[ ! -z "$SYNC_DRY_RUN" ]]; then
        options=(${options[@]} --dry-run)
    fi
    git pull "${options[@]}"
    echo ""
}

dir_items=($(ls "$repos_dir"))
for dir_item in "${dir_items[@]}"; do
    item_path="$repos_dir/$dir_item"
    if [[ -d "$item_path/.git" ]]; then
        backup_repo "$item_path"
    fi
done
