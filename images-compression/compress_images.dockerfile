# alpine:3.6 adds ImageMagick 7.0.5-10 which yields good compression.
FROM alpine:3.6
WORKDIR /src
RUN apk --update add imagemagick python3 && rm -rf /var/cache/apk
COPY compress_images.py /usr

# Build
# docker build -t compress_images:<tag> -f compress_images.dockerfile .

# Use
# docker run -it --rm -v $PWD:/src compress_images:<tag> python3 /usr/compress_images.py *.jpg --quality 20 --out-dir tmp
# chown -R $USER:$USER tmp
