# Use uma imagem base oficial
FROM python:3.8-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
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
    libxfixes3 && \
    rm -rf /var/lib/apt/lists/*

# Instalar o Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Debugging step to check Chrome version
RUN google-chrome --version

# Baixar a versão correta do ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+') && \
    wget -q "https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

# Adicionar o código do bot
WORKDIR /app
COPY . .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar o bot
CMD ["python", "bot.py"]
