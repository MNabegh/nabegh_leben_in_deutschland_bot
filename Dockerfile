FROM python:3.10-slim

# Install Chrome & dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl chromium-driver chromium && \
    rm -rf /var/lib/apt/lists/*

# Set environment for Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your script
COPY script.py .

# Run your script
CMD ["python", "script.py"]
