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

# Install the latest Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Debugging step to check Chrome version
RUN google-chrome --version

# Baixar a versão correta do ChromeDriver
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.204/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -r chromedriver-linux64 chromedriver-linux64.zip

# Adicionar o código do bot
WORKDIR /app
COPY . .

# Exponha a porta que o Flask está usando
EXPOSE 5000

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar o bot
CMD ["python", "bot.py"]
