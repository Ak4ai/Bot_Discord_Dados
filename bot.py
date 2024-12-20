from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import re
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para capturar e verificar a última mensagem do grupo
def verificar_ultima_mensagem(driver):
    try:
        # Localiza todas as mensagens visíveis na conversa
        mensagens = driver.find_elements(By.CSS_SELECTOR, "span.selectable-text")
        
        if mensagens:
            # Obtém o texto da última mensagem
            ultima_mensagem = mensagens[-1].text
            print(f"Última mensagem: {ultima_mensagem}")  # Log para depuração

            # Verifica se a mensagem segue o formato "/xdyh"
            match_highest = re.match(r"(?i)(\d+)d(\d+)h([+-]\d+)?", ultima_mensagem)
            if match_highest:
                quantidade = int(match_highest.group(1))
                lados = int(match_highest.group(2))
                modificador = int(match_highest.group(3)) if match_highest.group(3) else 0

                if quantidade > 0 and lados > 0:
                    resultados = [random.randint(1, lados) for _ in range(quantidade)]
                    maior = max(resultados) + modificador
                    return f"Resultados: {resultados} | Maior Valor (com Modificador): {maior}"

            # Verifica se a mensagem segue o formato "/xdy"
            match = re.match(r"(?i)(\d+)d(\d+)([+-]\d+)?", ultima_mensagem)
            if match:
                quantidade = int(match.group(1))
                lados = int(match.group(2))
                modificador = int(match.group(3)) if match.group(3) else 0

                if quantidade > 0 and lados > 0:
                    resultados = [random.randint(1, lados) for _ in range(quantidade)]
                    soma = sum(resultados) + modificador
                    return f"Resultados: {resultados} | Modificador: {modificador} | Soma Total: {soma}"

            # Verifica se a mensagem segue o formato "/dx"
            match_single = re.match(r"(?i)d(\d+)([+-]\d+)?", ultima_mensagem)
            if match_single:
                lados = int(match_single.group(1))
                modificador = int(match_single.group(2)) if match_single.group(2) else 0

                if lados > 0:
                    resultado = random.randint(1, lados) + modificador
                    return f"Resultado: {resultado} (com Modificador: {modificador})"

        else:
            print("Nenhuma mensagem encontrada.")
    except Exception as e:
        print(f"Erro ao verificar a última mensagem: {e}")
    return None

# Função para enviar uma mensagem no WhatsApp Web
def enviar_mensagem(driver, mensagem):
    try:
        # Espera até que a caixa de texto esteja visível
        caixa_texto = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="10"]'))
        )
        caixa_texto.click()
        caixa_texto.send_keys(mensagem + Keys.ENTER)
        print(f"Mensagem enviada: {mensagem}")
    except Exception as e:
        print(f"Erro ao enviar a mensagem: {e}")

# Função para buscar e abrir um grupo pelo nome
def abrir_grupo(driver, nome_grupo):
    try:
        # Espera até que a caixa de pesquisa esteja visível
        caixa_pesquisa = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="3"]'))
        )
        caixa_pesquisa.click()
        caixa_pesquisa.send_keys(nome_grupo + Keys.ENTER)
        sleep(2)  # Aguarda a lista de resultados carregar

        # Seleciona o grupo na lista de resultados
        grupo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//span[@title='{nome_grupo}']"))
        )
        grupo.click()
        print(f"Grupo '{nome_grupo}' aberto com sucesso.")
    except Exception as e:
        print(f"Erro ao abrir o grupo '{nome_grupo}': {e}")

# Configurações do Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Modo headless para servidores
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")  # Desabilita a GPU
chrome_options.add_argument("--remote-debugging-port=9222")  # Porta para depuração remota

# Caminho do ChromeDriver
service = Service("/usr/local/bin/chromedriver")

# Inicializar o driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navega para o WhatsApp Web
driver.get("https://web.whatsapp.com")

# Espera até que a página do WhatsApp Web carregue completamente
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="3"]'))
)

# Aguarda o login do usuário
print("Faça Login Por Favor (apenas na primeira execução)")
while True:
    try:
        # Verifica se o WhatsApp Web foi carregado corretamente
        driver.find_element(By.CLASS_NAME, "landing-headerTitle")
    except:
        break

sleep(5)  # Aguarda a página carregar

# Solicita o nome do grupo ao usuário
nome_grupo = "Arquivos"
abrir_grupo(driver, nome_grupo)

# Loop para monitorar as mensagens e reagir à última mensagem
while True:
    resultado = verificar_ultima_mensagem(driver)
    if resultado is not None:
        enviar_mensagem(driver, str(resultado))
    sleep(5)  # Atraso de 5 segundos entre as verificações
