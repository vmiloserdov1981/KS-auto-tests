FROM 
WORKDIR /app
ADD . /app
RUN python --version && \
    pip install -U pip && \
    pip --version && \
    pip install -r /app/requirements.txt && \
    pip3 freeze
    