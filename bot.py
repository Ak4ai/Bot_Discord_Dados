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
        mensagens = driver.find_elements(By.CSS_SELECTOR, "span.selectable-text")
        if mensagens:
            ultima_mensagem = mensagens[-1].text
            logger.info(f"Última mensagem: {ultima_mensagem}")

            match_highest = re.match(r"(?i)(\d+)d(\d+)h([+-]\d+)?", ultima_mensagem)
            if match_highest:
                quantidade = int(match_highest.group(1))
                lados = int(match_highest.group(2))
                modificador = int(match_highest.group(3)) if match_highest.group(3) else 0

                if quantidade > 0 and lados > 0:
                    resultados = [random.randint(1, lados) for _ in range(quantidade)]
                    maior = max(resultados) + modificador
                    return f"Resultados: {resultados} | Maior Valor (com Modificador): {maior}"

            match = re.match(r"(?i)(\d+)d(\d+)([+-]\d+)?", ultima_mensagem)
            if match:
                quantidade = int(match.group(1))
                lados = int(match.group(2))
                modificador = int(match.group(3)) if match.group(3) else 0

                if quantidade > 0 and lados > 0:
                    resultados = [random.randint(1, lados) for _ in range(quantidade)]
                    soma = sum(resultados) + modificador
                    return f"Resultados: {resultados} | Modificador: {modificador} | Soma Total: {soma}"

            match_single = re.match(r"(?i)d(\d+)([+-]\d+)?", ultima_mensagem)
            if match_single:
                lados = int(match_single.group(1))
                modificador = int(match_single.group(2)) if match_single.group(2) else 0

                if lados > 0:
                    resultado = random.randint(1, lados) + modificador
                    return f"Resultado: {resultado} (com Modificador: {modificador})"

        logger.info("Nenhuma mensagem válida encontrada.")
    except Exception as e:
        logger.error(f"Erro ao verificar a última mensagem: {e}")
    return None

# Função para enviar uma mensagem no WhatsApp Web
def enviar_mensagem(driver, mensagem):
    try:
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
        caixa_pesquisa = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="3"]'))
        )
        caixa_pesquisa.click()
        caixa_pesquisa.send_keys(nome_grupo + Keys.ENTER)
        sleep(2)

        grupo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//span[@title='{nome_grupo}']"))
        )
        grupo.click()
        logger.info(f"Grupo '{nome_grupo}' aberto com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao abrir o grupo '{nome_grupo}': {e}")

# Configuração do WebDriver com Selenium
chrome_driver_path = "/usr/local/bin/chromedriver" if os.name != 'nt' else "C://chromedriver/chromedriver.exe"
service = Service(chrome_driver_path)
options = Options()

profile_path = os.path.join(os.path.dirname(__file__), "profilepath")
options.add_argument(f"user-data-dir={profile_path}")
#options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
#options.add_argument("--headless=new")
options.add_argument("--start-maximized")  # Reduz travamentos no modo headless
options.add_argument("--disable-notifications")  # Previne notificações do navegador

# Ajuste do número máximo de conexões
os.environ['MAX_CONNECTIONS'] = "5"  # Limita conexões paralelas

driver = webdriver.Chrome(service=service, options=options)

# Função para recarregar automaticamente o site
def auto_reload(driver):
    try:
        driver.refresh()
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="3"]'))
        )
        logger.info("Página recarregada com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao recarregar a página: {e}")

# Navega para o WhatsApp Web
driver.get("https://web.whatsapp.com")

WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="3"]'))
)

logger.info("Faça Login Por Favor (apenas na primeira execução)")
while True:
    try:
        driver.find_element(By.CLASS_NAME, "landing-headerTitle")
    except:
        break

sleep(5)

nome_grupo = "Arquivos"
abrir_grupo(driver, nome_grupo)

# Verifica se a aba está funcional
def verificar_aba(driver):
    try:
        driver.title
        return True
    except:
        logger.warning("A aba travou. Tentando recarregar...")
        auto_reload(driver)
        return False

# Loop otimizado para monitorar mensagens
while True:
    if not verificar_aba(driver):
        continue
    resultado = verificar_ultima_mensagem(driver)
    if resultado is not None:
        enviar_mensagem(driver, str(resultado))
    sleep(10)  # Intervalo aumentado para reduzir uso de CPU
