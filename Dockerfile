FROM selenium/standalone-chrome:3.141.59
USER root
ADD . /app
WORKDIR /app

RUN apt-get update && \
    sudo ln -fs /usr/bin/python3.6 /usr/bin/python && \
    apt-get install -y python3-pip && \
    python --version && \
    pip3 --version && \
    pip3 install -r requirements.txt && \
    pip3 freeze && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER seluser