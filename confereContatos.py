from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import json

def ler_clientes():
    """
    Lê o arquivo JSON e retorna uma lista com todos os nomes dos clientes
    Returns:
        list: Lista de nomes dos clientes
    """
    try:
        with open('transportadoras_organizadas.json', 'r', encoding='utf-8') as file:
            dados = json.load(file)
            clientes = []
            for transportadora in dados:
                for cliente in transportadora.get('clientes', []):
                    clientes.append(cliente['nome'])
            return clientes
    except Exception as e:
        print(f"Erro ao ler arquivo JSON: {str(e)}")
        return []

def buscar_cliente(driver, wait, nome_cliente):
    """
    Busca um cliente específico no sistema
    """
    try:
        print(f"\nTentando buscar cliente: {nome_cliente}")
        
        # Garantir que estamos no frame correto
        try:
            driver.switch_to.default_content()
            iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            driver.switch_to.frame(iframe)
            print("Mudou para o frame correto")
        except Exception as e:
            print(f"Erro ao mudar para o frame: {str(e)}")
            return

        # Encontrar e preencher o campo de busca
        try:
            search_input = wait.until(EC.presence_of_element_located((By.ID, "SC_fast_search_top")))
            search_input.clear()
            time.sleep(1)
            search_input.send_keys(nome_cliente)
            print(f"Campo de busca preenchido com: {nome_cliente}")
            time.sleep(1)

            # Clicar no botão de busca
            search_button = wait.until(EC.element_to_be_clickable((By.ID, "SC_fast_search_submit_top")))
            search_button.click()
            print("Clicou no botão de busca")
            time.sleep(2)

        except Exception as e:
            print(f"Erro ao preencher campo de busca ou clicar no botão: {str(e)}")
            return

        # Verificar se o contato foi encontrado
        try:
            # Tentar encontrar o ícone de comentário verde
            comment_icon = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "i.fa-comment-dots[style*='color:#27ae60']")))
            print(f"Contato encontrado para {nome_cliente}")
            # Clicar no ícone de comentário
            comment_icon.click()
            print("Clicou no ícone de comentário")
            time.sleep(2)
            
            # Clicar no botão "Sim, Abrir!"
            botao_abrir = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled")))
            botao_abrir.click()
            print("Clicou no botão 'Sim, Abrir!'")
            time.sleep(2)
            
            # Selecionar a opção TRACKEN no select
            select = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select.swal2-select")))
            select_element = Select(select)
            select_element.select_by_value("768,S,2,38790-38791,1")
            print("Selecionou a opção TRACKEN")
            time.sleep(2)
            
            # Clicar no botão após selecionar TRACKEN
            botao_confirmar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled")))
            botao_confirmar.click()
            print("Clicou no botão de confirmação")
            time.sleep(2)
            
            # Clicar no botão OK
            botao_ok = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled")))
            botao_ok.click()
            print("Clicou no botão OK")
            time.sleep(3)  # Aumentei o tempo de espera aqui
            
            # Selecionar a opção Atendimento no select de departamento (Select2)
            try:
                # Garantir que estamos no frame correto novamente
                driver.switch_to.default_content()
                iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
                driver.switch_to.frame(iframe)
                
                # Selecionar departamento
                try:
                    # Primeira tentativa: Clicar no span e depois na opção
                    span_select2 = wait.until(EC.element_to_be_clickable((By.ID, "select2-id_sc_field_depart-container")))
                    driver.execute_script("arguments[0].click();", span_select2)
                    print("Clicou para abrir o select de departamento")
                    time.sleep(2)
                    
                    # Tentar encontrar e clicar na opção de várias formas
                    try:
                        opcao = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li[data-select2-id='11']")))
                        driver.execute_script("arguments[0].click();", opcao)
                    except:
                        try:
                            opcao = driver.find_element(By.XPATH, "//li[contains(text(), 'Atendimento')]")
                            driver.execute_script("arguments[0].click();", opcao)
                        except:
                            # Se não conseguir clicar, tentar selecionar diretamente
                            driver.execute_script("""
                                var select = document.getElementById('id_sc_field_depart');
                                select.value = '38790';
                                select.dispatchEvent(new Event('change'));
                            """)
                    
                    print("Selecionou a opção Atendimento")
                    time.sleep(2)
                    
                    # Selecionar atendente
                    try:
                        # Clicar no select de atendente
                        atendente_span = wait.until(EC.element_to_be_clickable((By.ID, "select2-id_sc_field_atendent-container")))
                        driver.execute_script("arguments[0].click();", atendente_span)
                        print("Clicou para abrir o select de atendente")
                        time.sleep(2)
                        
                        # Selecionar o atendente Marcos Sales
                        try:
                            opcao_atendente = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Marcos Sales')]")))
                            driver.execute_script("arguments[0].click();", opcao_atendente)
                        except:
                            # Se não conseguir clicar, tentar selecionar diretamente
                            driver.execute_script("""
                                var select = document.getElementById('id_sc_field_atendent');
                                select.value = 'marcossales.tracken@gmail.com';
                                select.dispatchEvent(new Event('change'));
                            """)
                        print("Selecionou o atendente")
                        time.sleep(2)
                    except Exception as e:
                        print(f"Erro ao selecionar atendente: {str(e)}")
                    
                except Exception as e:
                    print(f"Erro ao tentar selecionar departamento: {str(e)}")
                
            except Exception as e:
                print(f"Erro ao selecionar departamento: {str(e)}")
            
        except:
            # Se não encontrar o ícone, verificar se é mensagem de "não encontrado"
            try:
                not_found = wait.until(EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'Registros não encontrados')]")))
                print(f"Contato não encontrado para {nome_cliente}")
            except:
                print("Não foi possível determinar se o contato foi encontrado ou não")
        
        time.sleep(2)  # Pequena pausa antes de prosseguir
        
    except Exception as e:
        print(f"Erro geral ao buscar cliente {nome_cliente}: {str(e)}")

def fazer_login():
    """
    Função que realiza o login no site e retorna o driver e wait configurados
    Returns:
        tuple: (driver, wait) - O driver do Chrome e o objeto wait configurado
    """
    # Configurar opções do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    # Adicionar configuração para lidar com notificações
    chrome_options.add_argument("--disable-notifications")
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    
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
        print("Login realizado com sucesso!")
        
        # Aguardar e clicar no botão Ok após o login
        time.sleep(5)  # Aguarda a página carregar
        print("Procurando o botão Ok na nova página...")
        driver.switch_to.default_content()  # Volta para o contexto principal
        ok_button = wait.until(EC.element_to_be_clickable((By.ID, "sub_form_b")))
        ok_button.click()
        print("Clicou no botão Ok com sucesso!")
        time.sleep(3)
        
        # Clicar no link de Contatos
        print("Procurando o link de Contatos...")
        contatos_link = wait.until(EC.element_to_be_clickable((By.ID, "ListaContato")))
        contatos_link.click()
        print("Modal de contatos aberto com sucesso!")
        time.sleep(3)
        
        # Ler clientes do arquivo JSON
        clientes = ler_clientes()
        if clientes:
            print(f"\nEncontrados {len(clientes)} clientes para buscar")
            for i, cliente in enumerate(clientes, 1):
                print(f"\n{'='*50}")
                print(f"Cliente {i} de {len(clientes)}")
                print(f"{'='*50}")
                buscar_cliente(driver, wait, cliente)
        else:
            print("Nenhum cliente encontrado no arquivo JSON")
        
        return driver, wait
        
    except Exception as e:
        print(f"Erro ao fazer login ou acessar contatos: {str(e)}")
        driver.quit()
        return None, None

if __name__ == "__main__":
    # Exemplo de uso
    driver, wait = fazer_login()
    if driver:
        print("\nProcesso finalizado com sucesso!")
        input("Pressione Enter para fechar o navegador...")
        driver.quit()
    else:
        print("Falha no processo!") 