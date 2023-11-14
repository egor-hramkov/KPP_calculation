FROM python:3.10-alpine as build

ENV WORKDIR=/usr/src/app

WORKDIR ${WORKDIR}

COPY . ${WORKDIR}

RUN apk update \
        && apk --no-cache add \
            gcc \
            g++ \
            linux-headers \
            musl-dev \
            openssl-dev \
            zlib-dev \
            python3-dev \
            libpng-dev \
            freetype-dev \
            python3 \
            make \
            subversion \
            gfortran \
            ca-certificates \
            ln -s /usr/include/locale.h /usr/include/xlocale.h; python3 -m pip install matplotlib
