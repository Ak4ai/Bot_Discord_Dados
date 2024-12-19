# Usar a imagem base do Python
FROM python:3.10-slim

# Instalar dependências do sistema para rodar o Chrome headless
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    libx11-dev \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libnss3 \
    libxss1 \
    libgconf-2-4 \
    libfontconfig1 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libasound2 \
    libnspr4 \
    libdbus-glib-1-2 \
    && rm -rf /var/lib/apt/lists/*

# Baixar e instalar o Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb || apt-get -y --fix-broken install

# Instalar o pip e dependências do Python
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o código da aplicação
COPY . .

# Comando para rodar a aplicação
CMD ["python", "bot_whatsapp.py"]
