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
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

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
            logger.info(f"Última mensagem: {ultima_mensagem}")

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
            logger.info("Nenhuma mensagem encontrada.")
    except Exception as e:
        logger.error(f"Erro ao verificar a última mensagem: {e}")
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
        logger.info(f"Mensagem enviada: {mensagem}")
    except Exception as e:
        logger.error(f"Erro ao enviar a mensagem: {e}")

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
        logger.info(f"Grupo '{nome_grupo}' aberto com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao abrir o grupo '{nome_grupo}': {e}")

# Função para verificar se a aba está funcional
def verificar_aba(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, "div[data-tab='3']")
        return True
    except (WebDriverException, TimeoutException):
        return False

def recarregar_pagina(driver):
    try:
        driver.refresh()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-tab='3']")))
        return True
    except (WebDriverException, TimeoutException):
        return False

# Função para garantir que o login seja feito novamente, se necessário
def verificar_login(driver):
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "landing-headerTitle"))
        )
        logger.info("Requer login. Aguardando...")
        sleep(10)  # Tempo para o usuário escanear o QR Code
        return True
    except TimeoutException:
        logger.info("Já logado no WhatsApp Web.")
        return False

def iniciar_driver():
    chrome_driver_path = "/usr/local/bin/chromedriver" if os.name != 'nt' else "C://chromedriver/chromedriver.exe"
    service = Service(chrome_driver_path)
    options = Options()

    # Diretório onde os dados do perfil do Chrome serão salvos
    profile_path = os.path.join(os.path.dirname(__file__), "profilepath")  # Caminho relativo ao diretório do script
    options.add_argument(f"user-data-dir={profile_path}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--disable-gpu")  # Desativa aceleração de hardware
    options.add_argument("--disable-software-rasterizer")  # Previne erros gráficos  
    options.add_argument("--headless=new")  # Esxecuta sem interface gráfica
    options.add_argument("--headless")  # Adiciona a opção headless

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://web.whatsapp.com")

    # Espera até que a página do WhatsApp Web carregue completamente
    verificar_login(driver)

    # Aguarda o login do usuário
    logger.info("Faça Login Por Favor (apenas na primeira execução)")
    while True:
        try:
            # Verifica se o WhatsApp Web foi carregado corretamente
            driver.find_element(By.CLASS_NAME, "landing-headerTitle")
        except:
            break

    sleep(5)  # Aguarda a página carregar
    return driver

if __name__ == "__main__":
    driver = iniciar_driver()

    # Solicita o nome do grupo ao usuário
    nome_grupo = input("Digite o nome do grupo: ")
    abrir_grupo(driver, nome_grupo)

    try:
        while True:
            if not verificar_aba(driver):
                logger.warning("Aba do WhatsApp não está funcional. Tentando recarregar a página.")
                if not recarregar_pagina(driver):
                    logger.error("Falha ao recarregar a página. Reiniciando o WebDriver.")
                    driver.quit()
                    driver = iniciar_driver()
                    abrir_grupo(driver, nome_grupo)  # Reabre o grupo após reiniciar o WebDriver
                    continue

            # Chame a função para verificar a última mensagem
            resultado = verificar_ultima_mensagem(driver)
            if resultado is not None:
                enviar_mensagem(driver, str(resultado))

            sleep(1)  # Ajuste o tempo de espera conforme necessário

    except KeyboardInterrupt:
        logger.info("Interrupção manual detectada. Encerrando o bot.")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
    finally:
        driver.quit()