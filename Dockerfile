# Usando uma imagem base com Python
FROM python:3.11-slim

# Instalar dependências necessárias para o Selenium e o Chromium
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
    chromium \
    chromium-driver

# Atualize o pip
RUN pip install --upgrade pip

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto
COPY . .

# Instalar as dependências do Python
RUN pip install -r requirements.txt

# Configurar a variável de ambiente para o caminho do binário do Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER=/usr/bin/chromedriver

# Comando de execução do container
CMD ["python", "bot.py"]
