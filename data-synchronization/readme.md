Zip storage

```bash
zip_dir /path/to/_data /path/to/data/data.zip
```

Backup notes

```bash
sync_dir_dir /path/to/notes /disk/notes
```

Backup to cloud.

```bash
AWS_PROFILE=backup-profile backup_disk_cloud disk backup-bucket
```

Backup to disks.

```bash
backup_disk_disk misc_disk misc_backup_disk
backup_disk_disk media_disk media_backup_disk
backup_disk_disk media_backup_disk misc_backup_disk
```