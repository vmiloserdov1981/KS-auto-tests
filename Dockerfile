FROM python:3.8-alpine
WORKDIR /app
ADD . /app
RUN apk update && \
    apk add curl && \
    python --version && \
    pip install -U pip && \
    pip --version && \
    pip install -r /app/requirements.txt && \
    pip3 freeze && \
    curl -s https://aerokube.com/cm/bash | sh && \ 
    ls /bin/sh
    