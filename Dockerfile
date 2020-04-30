FROM python:3.8-alpine
WORKDIR /app
ADD . /app
RUN apk update && \
    python --version && \
    pip install -U pip && \
    pip --version && \
    pip install -r /app/requirements.txt
    