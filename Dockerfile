FROM python:3.8-buster
WORKDIR /app
ADD . /app
RUN python --version && \
    pip install -U pip && \
    pip --version && \
    pip install -r /app/requirements.txt && \
    pip3 freeze && \
    curl -s https://aerokube.com/cm/bash | bash && \ 
    ls /bin/bash
    