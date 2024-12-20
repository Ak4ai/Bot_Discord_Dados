# Escolha a imagem base (Ubuntu 20.04 como exemplo)
FROM ubuntu:20.04

# Configurar o fuso horário para evitar problemas durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Atualizar e instalar dependências do sistema
RUN apt-get update && apt-get install -y \
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
    python3-pip \
    unzip \
    curl \
    && apt-get clean

# Atualizar o pip
RUN pip3 install --no-cache-dir --upgrade pip

# Baixar e instalar o Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Verificar a versão do Google Chrome
RUN google-chrome --version

# Baixar e instalar o ChromeDriver correspondente
RUN CHROME_DRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -N https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

# Verificar a versão do ChromeDriver
RUN chromedriver --version

# Configurar o diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para o container
COPY . .

# Instalar as dependências do Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Comando para iniciar o bot
CMD ["python3", "bot.py"]
