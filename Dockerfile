FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3-pip python3.12-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install -r requirements.txt

# RUN /opt/venv/bin/python -m playwright install

# RUN /opt/venv/bin/python -m playwright install-deps