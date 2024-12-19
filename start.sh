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
    libxrandr2 \
    chromium \
    chromium-driver

# Atualizar o pip
pip install --upgrade pip

# Instalar as dependências do Python
pip install -r requirements.txt

# Configurar a variável de ambiente para o caminho do binário do Chrome
export CHROME_BIN=$(which chromium)
export CHROME_DRIVER=$(which chromedriver)

# Iniciar o bot
python bot.py