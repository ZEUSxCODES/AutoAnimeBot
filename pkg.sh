#!/bin/bash

# Install system dependencies
set -e # exit on error
if [[ ! $(command -v mediainfo) ]]; then
    sudo apt-get update
    sudo apt-get install -y mediainfo ffmpeg
fi

# Install Python dependencies
if [[ ! $(command -v pip3) || ! -x "$(command -v pip3)" ]]; then
    echo "pip3 not found, installing pip3"
    sudo apt-get install -y python3-pip
fi

pip3 install --upgrade -r requirements.txt
