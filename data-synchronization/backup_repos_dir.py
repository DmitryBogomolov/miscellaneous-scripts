#!/usr/bin/env python3

import os
from os import path
import util

def backup_repo(repo_path: str, is_dry_run: bool) -> None:
    ret = util.call_proc(['git', 'config', 'remote.origin.url'], capture_output=True, cwd=repo_path)
    remote_url = ret.stdout.strip()
    print(f'### "{remote_url}" --> "{repo_path}"')
    proc_args = ['git', 'pull', '--prune', '--verbose', '--force', '--ff-only', '--stat', 'origin', 'master']
    if is_dry_run:
        proc_args.append('--dry-run')
    util.call_proc(proc_args, cwd=repo_path)
    print('')

def backup_repos_dir(repos_path: str, dry_run: bool) -> None:
    repos_dir = path.abspath(repos_path)
    is_dry_run = util.is_dry_run(dry_run)

    util.check_dir_exist(repos_dir)

    repo_dirs = []
    for item in os.listdir(repos_dir):
        repo_dir = path.join(repos_dir, item)
        if path.isdir(path.join(repo_dir, '.git')):
            repo_dirs.append(repo_dir)

    for repo_dir in repo_dirs:
        backup_repo(repo_dir, is_dry_run)

def main() -> None:
    def setup_args(parser: util.ArgumentParser):
        parser.add_argument('repos_dir', help='repositories directory')
    args = util.parse_cmd_args(
        'Synchronizes repositories.',
        setup_args,
        add_dry_run=True
    )

    util.measure_time(lambda: backup_repos_dir(args.repos_dir, args.dry_run))

if __name__ == '__main__':
    main()
