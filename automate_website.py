from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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