# alpine:3.6 adds ImageMagick 7.0.5-10 which yields good compression.
FROM alpine:3.6
WORKDIR /src
RUN apk --update add imagemagick python3 && rm -rf /var/cache/apk
COPY compress_images.py /usr/local/bin/compress_images
RUN chmod +x /usr/local/bin/compress_images

# Build
# docker build -t compress_images:<tag> .

# Run
# docker run -it --rm -v $PWD:/src -u 1000:1000 compress_images:<tag> compress_images --quality 20 --out-dir tmp *.jpg
