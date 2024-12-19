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

# Configuração do WebDriver com Selenium
chrome_driver_path = "C:/chromedriver/chromedriver.exe"
service = Service(chrome_driver_path)
options = Options()

# Diretório onde os dados do perfil do Chrome serão salvos
profile_path = "C:/WhatsAppProfile"  # Substitua por um caminho válido no seu sistema
options.add_argument(f"user-data-dir={profile_path}")

# Inicializa o WebDriver
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://web.whatsapp.com/")

# Aguarda o login do usuário
print("Faça Login Por Favor (apenas na primeira execução)")
while True:
    try:
        # Verifica se o WhatsApp Web foi carregado corretamente
        driver.find_element(By.CLASS_NAME, "landing-headerTitle")
    except:
        break

sleep(5)  # Aguarda a página carregar

# Aguarda o usuário abrir o grupo
print("Agora, Abra o Grupo que deseja Monitorar")
input("Você já está pronto? Pressione Enter para continuar...")

# Loop para monitorar as mensagens e reagir à última mensagem
while True:
    resultado = verificar_ultima_mensagem(driver)
    if resultado is not None:
        enviar_mensagem(driver, str(resultado))
    sleep(5)  # Atraso de 5 segundos entre as verificações
