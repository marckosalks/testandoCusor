from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fazer_login():
    """
    Função que realiza o login no site e retorna o driver e wait configurados
    Returns:
        tuple: (driver, wait) - O driver do Chrome e o objeto wait configurado
    """
    # Configurar opções do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    
    # Inicializar o driver do Chrome
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)
    
    try:
        print("Abrindo o site...")
        driver.get("https://new.bitsac.com.br/")
        time.sleep(3)
        
        # Login no site
        print("Fazendo login...")
        iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe)
        
        # Preencher email
        email_field = wait.until(EC.presence_of_element_located((By.ID, "id_sc_field_login")))
        email_field.clear()
        email_field.send_keys("marcossales.tracken@gmail.com")
        
        # Preencher senha
        password_field = wait.until(EC.presence_of_element_located((By.ID, "id_sc_field_pswd")))
        password_field.clear()
        password_field.send_keys("marcostracken02")
        
        # Clicar no botão de login
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "btnlogarr")))
        login_button.click()
        time.sleep(3)
        
        print("Login realizado com sucesso!")
        return driver, wait
        
    except Exception as e:
        print(f"Erro ao fazer login: {str(e)}")
        driver.quit()
        return None, None

if __name__ == "__main__":
    # Exemplo de uso
    driver, wait = fazer_login()
    if driver:
        print("Login bem sucedido! Você pode continuar com outras operações.")
        # Aqui você pode adicionar outras operações que precise fazer
        input("Pressione Enter para fechar o navegador...")
        driver.quit()
    else:
        print("Falha no login!") 