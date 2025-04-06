from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os

def login_website():
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Maximize the browser window
    
    # Initialize the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("Abrindo o site...")
        # Open the website
        driver.get("https://new.bitsac.com.br/")
        
        # Wait for the page to load
        print("Aguardando carregamento da página...")
        time.sleep(5)
        
        # Wait for the iframe to be present and switch to it
        print("Procurando o iframe...")
        wait = WebDriverWait(driver, 20)
        iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        print("Iframe encontrado, mudando para o contexto do iframe...")
        driver.switch_to.frame(iframe)
        
        # Print the current page source to see what's inside the iframe
        print("Conteúdo do iframe:", driver.page_source)
        
        # Wait for the login elements to be present and clickable
        print("Procurando campos de login...")
        wait = WebDriverWait(driver, 20)
        
        try:
            # Find and fill the email field using the correct selector
            print("Tentando encontrar o campo de email...")
            email_field = wait.until(EC.presence_of_element_located((By.ID, "id_sc_field_login")))
            print("Campo de email encontrado, preenchendo...")
            email_field.clear()
            email_field.send_keys("marcossales.tracken@gmail.com")
            
            # Find and fill the password field using the correct selector
            print("Tentando encontrar o campo de senha...")
            password_field = wait.until(EC.presence_of_element_located((By.ID, "id_sc_field_pswd")))
            print("Campo de senha encontrado, preenchendo...")
            password_field.clear()
            password_field.send_keys("marcostracken02")
            
            # Find and click the login button using the correct ID
            print("Tentando encontrar o botão de login...")
            login_button = wait.until(EC.element_to_be_clickable((By.ID, "btnlogarr")))
            print("Botão de login encontrado, clicando...")
            login_button.click()
            
            # Wait for the Ok button to appear and click it using JavaScript
            print("Aguardando botão Ok aparecer...")
            ok_button = wait.until(EC.presence_of_element_located((By.ID, "sub_form_b")))
            print("Botão Ok encontrado, executando clique via JavaScript...")
            driver.execute_script("arguments[0].click();", ok_button)
            
            # Switch back to the main content
            print("Voltando para o contexto principal...")
            driver.switch_to.default_content()
            
            # Wait for login to complete
            print("Aguardando processamento do login...")
            time.sleep(10)
            
            # Navigate to the chat page
            print("Navegando para a página do chat...")
            driver.get("https://new.bitsac.com.br/blank_chat_v2/blank_chat_v2.php")
            time.sleep(5)
            
            # Find and click the add account icon
            print("Procurando ícone de adicionar conta...")
            add_account_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "i.mdi.mdi-account-plus")))
            print("Ícone encontrado, clicando...")
            add_account_icon.click()
            
            # Wait for the name field to appear
            print("Aguardando campo de nome aparecer...")
            time.sleep(3)
            
            # Read the JSON file
            print("Lendo arquivo JSON...")
            json_path = 'transportadoras_organizadas.json'
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        print("Conteúdo do JSON:", data)
                        nome = data.get('nome', '')
                        if not nome:
                            print("Aviso: Campo 'nome' não encontrado no JSON")
                            nome = "Nome Padrão"  # Valor padrão caso não encontre o nome
                except json.JSONDecodeError as e:
                    print(f"Erro ao ler o JSON: {str(e)}")
                    nome = "Nome Padrão"
            else:
                print(f"Arquivo {json_path} não encontrado")
                nome = "Nome Padrão"
            
            # Find and fill the name field using JavaScript
            print("Procurando campo de nome...")
            nome_field = wait.until(EC.presence_of_element_located((By.ID, "id_sc_field_nome")))
            print("Campo de nome encontrado, preenchendo...")
            
            # Clear the field using JavaScript
            driver.execute_script("arguments[0].value = '';", nome_field)
            
            # Fill the field using JavaScript
            driver.execute_script(f"arguments[0].value = '{nome}';", nome_field)
            
            # Trigger input event to ensure the field is updated
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", nome_field)
            
            # Keep the browser open for 30 seconds
            print("Mantendo o navegador aberto por 30 segundos...")
            time.sleep(30)
            
        except Exception as e:
            print(f"Erro ao tentar preencher o formulário: {str(e)}")
            print("Tentando encontrar elementos alternativos...")
            # Try to find all input fields
            inputs = driver.find_elements(By.TAG_NAME, "input")
            print(f"Inputs encontrados: {len(inputs)}")
            for input_elem in inputs:
                print(f"Input encontrado: {input_elem.get_attribute('outerHTML')}")
            
    except Exception as e:
        print(f"Erro principal: {str(e)}")
        print("Page source:", driver.page_source)
    
    finally:
        print("Fechando o navegador...")
        driver.quit()

if __name__ == "__main__":
    login_website() 