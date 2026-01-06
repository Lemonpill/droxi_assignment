FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install a minimal set of system deps required by Playwright browsers
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    curl wget ca-certificates gnupg apt-transport-https build-essential \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libx11-6 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0 libgtk-3-0 libxss1 libdrm2 libxshmfence1 fonts-liberation \
  && rm -rf /var/lib/apt/lists/*

# Use generated requirements.txt (created from pipenv by the developer)
COPY requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip \
  && pip install -r /app/requirements.txt

# Copy project files
COPY . /app

# Install Playwright browsers and required system packages
RUN python -m playwright install --with-deps

# Ensure reports dir exists
RUN mkdir -p /app/reports/allure-results

ENTRYPOINT ["pytest", "-q"]
