FROM python:3.9-alpine
ARG CLIKRAKEN_VERSION
ARG CLIKRAKEN_URL

RUN apk update && apk upgrade && \
    apk add --no-cache git

RUN adduser -D clikraken
USER clikraken

RUN mkdir -p ~/.venv && \
    python3 -m venv ~/.venv/clikraken && \
    source ~/.venv/clikraken/bin/activate && \
    case $CLIKRAKEN_URL in \
      http*) pip --no-cache-dir install git+$CLIKRAKEN_URL@$CLIKRAKEN_VERSION;; \
      *) pip --no-cache-dir install git+$(echo $CLIKRAKEN_URL|sed -e 's@.*:@https://github.com/@')@$CLIKRAKEN_VERSION;; \
    esac && \
    mkdir -p ~/.config/clikraken

WORKDIR /home/clikraken
VOLUME ["/home/clikraken/.config/clikraken"]
ENTRYPOINT ["/home/clikraken/.venv/clikraken/bin/clikraken"]
CMD ["--help"]
