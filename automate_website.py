from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import os

def login_website():
    # Configurar opções do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Maximizar a janela do navegador
    
    # Inicializar o driver do Chrome
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("Abrindo o site...")
        # Abrir o site
        driver.get("https://new.bitsac.com.br/")
        
        # Aguardar o carregamento da página
        print("Aguardando carregamento da página...")
        time.sleep(5)
        
        # Aguardar o iframe estar presente e mudar para ele
        print("Procurando o iframe...")
        wait = WebDriverWait(driver, 20)
        iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        print("Iframe encontrado, mudando para o contexto do iframe...")
        driver.switch_to.frame(iframe)
        
        # Imprimir o código fonte atual para ver o que está dentro do iframe
        print("Conteúdo do iframe:", driver.page_source)
        
        # Aguardar os elementos de login estarem presentes e clicáveis
        print("Procurando campos de login...")
        wait = WebDriverWait(driver, 20)
        
        try:
            # Encontrar e preencher o campo de email
            print("Tentando encontrar o campo de email...")
            email_field = wait.until(EC.presence_of_element_located((By.ID, "id_sc_field_login")))
            print("Campo de email encontrado, preenchendo...")
            email_field.clear()
            email_field.send_keys("marcossales.tracken@gmail.com")
            
            # Encontrar e preencher o campo de senha
            print("Tentando encontrar o campo de senha...")
            password_field = wait.until(EC.presence_of_element_located((By.ID, "id_sc_field_pswd")))
            print("Campo de senha encontrado, preenchendo...")
            password_field.clear()
            password_field.send_keys("marcostracken02")
            
            # Encontrar e clicar no botão de login
            print("Tentando encontrar o botão de login...")
            login_button = wait.until(EC.element_to_be_clickable((By.ID, "btnlogarr")))
            print("Botão de login encontrado, clicando...")
            login_button.click()
            
            # Aguardar o carregamento após o login
            print("Aguardando carregamento após login...")
            time.sleep(10)

            # Voltar para o conteúdo principal
            driver.switch_to.default_content()

            # Aguardar o modal de adicionar contato aparecer
            print("Aguardando o modal de adicionar contato...")
            modal = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "swal2-popup")))
            
            # Encontrar e mudar para o iframe dentro do modal
            print("Procurando o iframe dentro do modal...")
            modal_iframe = wait.until(EC.presence_of_element_located((By.ID, "adicionar_contato_iframe")))
            driver.switch_to.frame(modal_iframe)
            
            # Ler o arquivo JSON com as transportadoras
            print("Lendo arquivo de transportadoras...")
            with open('transportadoras_organizadas.json', 'r', encoding='utf-8') as file:
                transportadoras = json.load(file)
            
            # Procurar a primeira transportadora que tenha clientes
            nome_cliente = None
            for transportadora in transportadoras:
                if transportadora.get('clientes') and len(transportadora['clientes']) > 0:
                    nome_cliente = transportadora['clientes'][0]['nome']
                    print(f"Cliente encontrado: {nome_cliente}")
                    break
            
            if nome_cliente:
                # Encontrar e preencher o campo de nome
                print("Procurando o campo de nome...")
                nome_field = wait.until(EC.presence_of_element_located((By.ID, "id_sc_field_nome")))
                print("Campo de nome encontrado, preenchendo...")
                nome_field.clear()
                nome_field.send_keys(nome_cliente)
                time.sleep(5)

                # Encontrar e preencher o campo de grupo
                print("Procurando o campo de grupo...")
                # Encontrar o elemento select2 pelo ID específico
                select2_container = wait.until(EC.presence_of_element_located((By.ID, "select2-id_sc_field_grupo-container")))
                print("Container do select2 encontrado, clicando...")
                
                # Clicar no container para abrir o dropdown
                select2_container.click()
                time.sleep(2)
                
                # Procurar a opção "Importados Agenda" no dropdown aberto
                print("Procurando a opção 'Importados Agenda'...")
                opcao_grupo = wait.until(EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Importados Agenda')]")))
                print("Opção encontrada, selecionando...")
                opcao_grupo.click()
                time.sleep(2)
            else:
                print("Nenhum cliente encontrado no arquivo JSON")
            
        except Exception as e:
            print(f"Erro ao tentar preencher o formulário: {str(e)}")
            print("Tentando encontrar elementos alternativos...")
            # Tentar encontrar todos os campos de input
            inputs = driver.find_elements(By.TAG_NAME, "input")
            print(f"Inputs encontrados: {len(inputs)}")
            for input_elem in inputs:
                print(f"Input encontrado: {input_elem.get_attribute('outerHTML')}")
            
    except Exception as e:
        print(f"Erro principal: {str(e)}")
        print("Código fonte da página:", driver.page_source)
    
    finally:
        print("Fechando o navegador...")
        driver.quit()

if __name__ == "__main__":
    login_website() 