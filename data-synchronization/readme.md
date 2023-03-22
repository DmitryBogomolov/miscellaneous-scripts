# Data Synchronization

Python wrappers over several commands - rsync, zip/unzip, gpg, git, s3 sync.

Synchronizes content between directories and with s3 storage. Encrypts/decrypts files and directories. Dumps git repositories.

----
Installation (copy to ~/.local/lib/data-synchronization and make symlinks in ~/.local/bin).
```bash
python3 setup.py on
python3 setup.py off
```

----
Backup storage
```bash
decrypt_dir /path/to/dump_dir.pgp
# update dump part
encrypt_dir /path/to/dump_dir
```

Backup notes
```bash
sync_dir_dir /path/to/notes /disk/notes
```

Backup repositories
```bash
backup_repos_dir /path/to/repos
```

Backup to cloud.
```bash
AWS_PROFILE=backup-profile backup_disk_cloud disk backup-bucket
```

Backup to disks.
```bash
backup_disk_disk misc_disk misc_backup_disk
backup_disk_disk media_disk media_backup_disk
```
