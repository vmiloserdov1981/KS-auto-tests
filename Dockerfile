FROM selenium/standalone-chrome:3.141.59
WORKDIR /app
ADD . /app
RUN sudo apt-get update && \
    sudo ln -fs /usr/bin/python3.6 /usr/bin/python && \
    sudo apt-get install -y python3-pip && \
    python --version && \
    pip3 --version && \
    sudo -H pip3 install -r /app/requirements.txt && \
    pip3 freeze && \
    sudo apt-get clean && \
    sudo rm -rf /var/lib/apt/lists/*
