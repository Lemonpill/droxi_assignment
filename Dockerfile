FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    software-properties-common curl gnupg ca-certificates build-essential apt-transport-https wget unzip git lsb-release \
  && add-apt-repository ppa:deadsnakes/ppa -y \
  && apt-get update \
  && apt-get install -y python3.13 python3.13-venv python3.13-dev python3-pip openjdk-11-jdk \
  && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
  && apt-get install -y nodejs \
  && python3.13 -m pip install --upgrade pip \
  && pip install pipenv playwright allure-pytest \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Pipfile first for dependency install layer
COPY Pipfile Pipfile.lock* /app/

RUN pip install --upgrade pip pipenv \
  && (pipenv install --system --deploy || pipenv install --system)

# Copy project files
COPY . /app

# Install Playwright browsers + system deps
RUN python3.13 -m playwright install --with-deps

# Ensure reports dir exists
RUN mkdir -p /app/reports/allure-results

ENTRYPOINT ["pytest", "-q"]
