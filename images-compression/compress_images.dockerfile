# alpine:3.6 adds ImageMagick 7.0.5-10 which yields good compression.
FROM alpine:3.6
WORKDIR /src
RUN apk --update add imagemagick python3 && rm -rf /var/cache/apk
COPY compress_images.py /usr

# Build
# docker build -t compress_images:<tag> -f compress_images.dockerfile .

# Run
# docker run -it --rm -v $PWD:/src -u 1000:1000 compress_images:<tag> python3 /usr/compress_images.py--quality 20 --out-dir tmp *.jpg
