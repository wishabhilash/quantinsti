#!/bin/bash

# Update repo cache
sudo apt update

# Create datafiles directory
mkdir datafiles

# APT installs
sudo apt install redis-server -y
sudo apt install virtualenv -y
sudo apt install python3-pip -y
sudo apt install mysql-server -y
# END

# Create python virtual environment
virtualenv --python=python3 .venv
. .venv/bin/activate
# END

# Install requirements.txt
pip install -r requirements.txt
# END