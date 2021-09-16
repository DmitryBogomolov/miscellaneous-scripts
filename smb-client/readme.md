Console client

```bash
smbclient smbclient //<server>/<root_dir> -U <user>
```

Create mount point

```bash
apt-get install cifs-utils
mkdir /mnt/<mount_dir>
```
```bash
mount -t cifs -o username="<user>",password="<pass>",vers=1.0,uid=$(id -u),gid=$(id -g) //<server>/<root_dir> /mnt/<mount_dir>

umount /mnt/<mount_dir>
```
