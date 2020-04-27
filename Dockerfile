FROM selenium/standalone-chrome:3.141.59

ADD . /app
WORKDIR /app

RUN sudo apt-get update && \
    sudo apt-get install -y python3-pip && \
    pip3 --version && \
    pip3 install -r requirements.txt && \
    sudo apt-get clean && \
    sudo rm -rf /var/lib/apt/lists/*