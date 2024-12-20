#!/bin/bash

# Atualizar e instalar dependências do sistema
apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    fontconfig \
    libx11-dev \
    libxkbcommon0 \
    libgdk-pixbuf2.0-0 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxdamage1 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libasound2 \
    libnss3 \
    libxtst6 \
    libxrandr2

# Atualizar o pip
pip install --upgrade pip

# Instalar as dependências do Python
pip install -r requirements.txt

# ...existing code...

# Instalar o Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb

# Verificar a versão do Chrome
google-chrome --version

# Verificar a versão do ChromeDriver
chromedriver --version

# Baixar o ChromeDriver correspondente
CHROME_DRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -N https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
rm chromedriver_linux64.zip

# Verificar a versão do ChromeDriver
chromedriver --version

# Iniciar o bot
python bot.py