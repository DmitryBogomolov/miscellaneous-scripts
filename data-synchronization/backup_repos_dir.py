#!/usr/bin/env python3

import os.path as path
import os
import time
import util

def backup_repo(repo_path, is_dry_run):
    ret = util.call_proc(['git', 'config', 'remote.origin.url'], capture_output=True, cwd=repo_path)
    remote_url = ret.stdout.strip()
    print('### "{}" --> "{}"'.format(remote_url, repo_path))
    proc_args = ['git', 'pull', '--prune', '--verbose', '--force', '--ff-only', '--stat']
    if is_dry_run:
        proc_args.append('--dry-run')
    util.call_proc(proc_args, cwd=repo_path)
    print('')

def backup_repos_dir(repos_path, dry_run):
    repos_dir = path.abspath(repos_path)
    is_dry_run = util.is_dry_run(dry_run)

    util.check_dir_exist(repos_dir)

    repo_dirs = []
    for item in os.listdir(repos_dir):
        repo_dir = path.join(repos_dir, item)
        if path.isdir(path.join(repo_dir, '.git')):
            repo_dirs.append(repo_dir)

    begin_time = time.time()
    for repo_dir in repo_dirs:
        backup_repo(repo_dir, is_dry_run)
    end_time = time.time()
    duration = int(end_time - begin_time)
    print('time: {}s'.format(duration))

def main():
    def setup_args(parser):
        parser.add_argument('repos_dir', help='repositories directory')
    args = util.parse_cmd_args(
        'Synchronizes repositories.',
        setup_args,
        add_dry_run=True
    )

    backup_repos_dir(args.repos_dir, args.dry_run)

if __name__ == '__main__':
    main()
