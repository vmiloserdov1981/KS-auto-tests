FROM selenium/standalone-chrome:3.141.59
USER root
ADD . /app
WORKDIR /app

RUN sudo apt-get update && \
    sudo sudo ln -fs /usr/bin/python3.6 /usr/bin/python && \
    sudo apt-get install -y python3-pip && \
    python --version && \
    pip3 --version && \
    sudo -H pip3 install -r requirements.txt && \
    pip3 freeze && \
    sudo apt-get clean && \
    sudo rm -rf /var/lib/apt/lists/*

USER seluser