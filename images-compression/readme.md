# Images Compression

Python wrapper over [convert](https://imagemagick.org/script/convert.php) command.

----
Installation (copy file without extension to ~/.local/bin and make it executable).
```bash
python3 setup.py on
python3 setup.py off
```

----
Usage
```bash
compress_images --quality 20 --out-dir tmp file-1.jpg file-2.jpg ... file-n.jpg
```

----
Building image
```bash
docker build -t compress_images:<tag> .
```

Running
```bash
docker run -it --rm -v $PWD:/src -u 1000:1000 compress_images:<tag> compress_images --quality 20 --out-dir tmp *.jpg
```
