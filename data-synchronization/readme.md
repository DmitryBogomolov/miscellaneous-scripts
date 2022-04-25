Backup storage
```bash
encrypt_file /path/to/dump_file
zip_dir /path/to/dump_file
# update dump part
zip_dir /path/to/dump_folder
encrypt_file /path/to/dump_file
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
