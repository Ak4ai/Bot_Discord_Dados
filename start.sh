#!/bin/bash

# Instalar o Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get update
apt-get install -y ./google-chrome-stable_current_amd64.deb

# Instalar o ChromeDriver
CHROME_VERSION=$(google-chrome --version | sed -E 's/[^0-9]*([0-9]+)\..*/\1/')
wget https://chromedriver.storage.googleapis.com/${CHROME_VERSION}.0/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/chromedriver
chmod +x /usr/local/bin/chromedriver


python bot.py
