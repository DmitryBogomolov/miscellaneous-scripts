# Video Helper

Python wrapper over [ffmpeg](https://ffmpeg.org/) command.

Converts files to *mp4* format. Joins *mp4* files.

----
Convert to *mp4*
```bash
python3 to_mp4.py file.avi
```

Convert several files simultaneously
```bash
python3 to_mp4_many.py file-1.avi file-2.avi ... file-n.avi
```

Join files
```bash
python3 join_files.py --out-file file.mp4 file-1.mp4 file-2.mp4 ... file-n.mp4
```

Convert several files and join them
```bash
python3 join_to_mp4.py --out-file file.mp4 file-1.avi file-2.avi ... file-n.avi
```
