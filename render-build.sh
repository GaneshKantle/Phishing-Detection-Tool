#!/bin/bash
# Upgrade pip to avoid version conflicts
pip install --upgrade pip

# Install system-level packages required for building
apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev
