#!/bin/sh

dir="$PWD"
uid="$(id -u)"
docker run -it --rm -u $uid:$uid -v $dir:/src compress_images compress_images "$@"
