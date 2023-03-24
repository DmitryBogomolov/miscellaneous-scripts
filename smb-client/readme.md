# Smb Client

Mounts remote smb drive to local directory.

----

Run client.

```bash
smbclient //<server>/<root_dir> -U <user>
```

Create mount point.

```bash
apt-get install cifs-utils
mkdir /mnt/<mount_dir>
```

Mount local directory.
```bash
mount -t cifs -o username="<user>",password="<pass>",vers=1.0,uid=$(id -u),gid=$(id -g) //<server>/<root_dir> /mnt/<mount_dir>

umount /mnt/<mount_dir>
```

With script.
```bash
bash smb_mount.sh //<server>/<root_dir> /mnt/<mount_dir> <user> <pass>
```
