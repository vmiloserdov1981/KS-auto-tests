FROM python:3.8-alpine
WORKDIR /app
ADD . /app
RUN apk update && \
    apk add docker && \
    rc-update add docker boot && \
    python --version && \
    pip install docker && \
    pip install -U pip && \
    pip --version && \
    pip install -r /app/requirements.txt
    