FROM python:3.8-alpine
WORKDIR /app
ADD . /app
RUN apk update && \
    apk install -y curl && \
    curl -s https://aerokube.com/cm/bash | bash && \ 
    python --version && \
    pip install -U pip && \
    pip --version && \
    pip install -r /app/requirements.txt && \
    pip3 freeze
    