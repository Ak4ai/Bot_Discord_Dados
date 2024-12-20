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

def verificar_aba(driver):
    try:
        # Tenta acessar o título da aba para verificar se está funcional
        driver.title
        return True
    except:
        print("A aba travou. Tentando recarregar...")
        driver.get("https://web.whatsapp.com/")
        return False

def verificar_sessao(driver):
    try:
        driver.find_element(By.CLASS_NAME, "landing-headerTitle")
        print("Sessão inválida. Por favor, revalide manualmente.")
        return False
    except:
        return True

# Configuração do WebDriver com Selenium
chrome_driver_path = "/usr/local/bin/chromedriver"  # Caminho do ChromeDriver no contêiner Docker
service = Service(chrome_driver_path)
options = Options()

# Diretório onde os dados do perfil do Chrome serão salvos
profile_path = os.path.join(os.path.dirname(__file__), "profilepath")  # Caminho relativo ao diretório do script
options.add_argument(f"user-data-dir={profile_path}")
options.add_argument("--headless")  # Adiciona a opção headless
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-dev-shm-usage")  # Usa espaço em disco no lugar de memória
options.add_argument("--disable-gpu")  # Desativa aceleração de hardware
options.add_argument("--disable-software-rasterizer")  # Previne erros gráficos
options.add_argument("--headless=new")  # Executa sem interface gráfica

driver = webdriver.Chrome(service=service, options=options)

# Navega para o WhatsApp Web
driver.get("https://web.whatsapp.com")

# ...existing code...
# Espera até que a página do WhatsApp Web carregue completamente
try:
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"][data-tab="3"]'))
    )
except TimeoutException:
    print("Timeout while waiting for the WhatsApp Web page to load.")
    print(driver.page_source)  # Print the page source for debugging
    driver.save_screenshot("screenshot.png")  # Save a screenshot for debugging
    driver.quit()
    exit(1)
# ...existing code...

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
    if not verificar_aba(driver):
        continue
    if not verificar_sessao(driver):
        input("Revalide a sessão manualmente e pressione Enter para continuar...")
    resultado = verificar_ultima_mensagem(driver)
    if resultado is not None:
        enviar_mensagem(driver, str(resultado))
    sleep(5)
