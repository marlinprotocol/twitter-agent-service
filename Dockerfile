FROM ubuntu:24.04

WORKDIR /app

RUN apt-get update && \
    apt-get install -y nodejs npm python3-pip python3.12-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

RUN python3 -m venv /opt/venv

# Install Python dependencies
RUN /opt/venv/bin/pip install -r requirements.txt

# Install Playwright dependencies
RUN npx playwright install --with-deps

# Run the application
CMD ["/opt/venv/bin/python", "twtagent.py"]