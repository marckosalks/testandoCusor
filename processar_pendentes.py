from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os

def processar_contato(driver, wait, cliente):
    """Processa um único contato, preenchendo o formulário"""
    try:
        # Encontrar e preencher o campo de nome
        print(f"Processando cliente: {cliente['nome']} (DDD: {cliente['ddd']})")
        nome_field = wait.until(EC.presence_of_element_located((By.ID, "id_sc_field_nome")))
        nome_field.clear()
        nome_field.send_keys(cliente['nome'])
        time.sleep(1)

        # Encontrar e preencher o campo de DDD
        ddd_field = wait.until(EC.presence_of_element_located((By.ID, "id_sc_field_dd")))
        ddd_field.clear()
        ddd_field.send_keys(cliente['ddd'])
        time.sleep(1)

        # Encontrar e preencher o campo de número de telefone
        numero_field = wait.until(EC.presence_of_element_located((By.ID, "id_sc_field_numero")))
        numero_field.clear()
        numero_field.send_keys(cliente['telefone'])
        time.sleep(1)

        # Selecionar a instância TRACKEN
        driver.execute_script("""
            var select = document.getElementById('id_sc_field_id_instancia');
            if (select) {
                var option = select.querySelector('option[value="768"]');
                if (option) {
                    option.selected = true;
                    var event = new Event('change', { bubbles: true });
                    select.dispatchEvent(event);
                }
            }
        """)
        time.sleep(1)

        # Selecionar o grupo
        select2_container = wait.until(EC.presence_of_element_located((By.ID, "select2-id_sc_field_grupo-container")))
        select2_container.click()
        time.sleep(1)
        opcao_grupo = wait.until(EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Importados Agenda')]")))
        opcao_grupo.click()
        time.sleep(1)

        # Selecionar etiquetas
        driver.execute_script("""
            var select = document.getElementById('id_sc_field_ids_etiquetas');
            if (select) {
                var option = select.querySelector('option[value="7001"]');
                if (option) {
                    option.selected = true;
                    var event = new Event('change', { bubbles: true });
                    select.dispatchEvent(event);
                }
            }
        """)
        time.sleep(1)

        # Clicar no botão Incluir
        botao_incluir = wait.until(EC.element_to_be_clickable((By.ID, "sc_b_ins_t")))
        botao_incluir.click()
        
        return True

    except Exception as e:
        print(f"Erro ao processar contato {cliente['nome']}: {str(e)}")
        return False

def processar_pendentes():
    # Carregar contatos pendentes
    try:
        with open('contatos_pendentes.json', 'r', encoding='utf-8') as file:
            contatos_pendentes = json.load(file)
    except FileNotFoundError:
        print("Arquivo de contatos pendentes não encontrado!")
        print("Execute primeiro o script verificar_progresso.py")
        return

    # Carregar contatos já processados
    processados = set()
    if os.path.exists('progresso_cadastro.json'):
        with open('progresso_cadastro.json', 'r', encoding='utf-8') as file:
            processados = set(json.load(file))

    # Configurar Chrome
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("Abrindo o site...")
        driver.get("https://new.bitsac.com.br/")
        time.sleep(3)
        
        # Login
        print("Fazendo login...")
        wait = WebDriverWait(driver, 20)
        iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe)
        
        email_field = wait.until(EC.presence_of_element_located((By.ID, "id_sc_field_login")))
        email_field.clear()
        email_field.send_keys("marcossales.tracken@gmail.com")
        
        password_field = wait.until(EC.presence_of_element_located((By.ID, "id_sc_field_pswd")))
        password_field.clear()
        password_field.send_keys("marcostracken02")
        
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "btnlogarr")))
        login_button.click()
        time.sleep(3)

        total_pendentes = len(contatos_pendentes)
        print(f"\nIniciando processamento de {total_pendentes} contatos pendentes...")
        
        ultimo_modal_processado = None
        processados_agora = 0
        
        while contatos_pendentes:  # Continua enquanto houver contatos pendentes
            try:
                # Voltar para o conteúdo principal e esperar o modal
                driver.switch_to.default_content()
                print("\nAguardando modal de contato...")
                
                # Esperar até que um novo modal apareça
                modal = None
                while True:
                    try:
                        modal = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "swal2-popup")))
                        if modal != ultimo_modal_processado:
                            break
                        time.sleep(1)
                    except:
                        time.sleep(1)
                        continue

                ultimo_modal_processado = modal
                
                # Encontrar e mudar para o iframe do modal
                modal_iframe = wait.until(EC.presence_of_element_located((By.ID, "adicionar_contato_iframe")))
                driver.switch_to.frame(modal_iframe)
                
                # Pegar próximo contato pendente
                cliente = contatos_pendentes.pop(0)  # Remove e retorna o primeiro contato da lista
                
                if processar_contato(driver, wait, cliente):
                    cliente_id = f"{cliente['ddd']}{cliente['telefone']}"
                    processados.add(cliente_id)
                    processados_agora += 1
                    
                    # Salvar progresso
                    with open('progresso_cadastro.json', 'w', encoding='utf-8') as file:
                        json.dump(list(processados), file)
                    
                    # Atualizar arquivo de pendentes
                    with open('contatos_pendentes.json', 'w', encoding='utf-8') as file:
                        json.dump(contatos_pendentes, file, ensure_ascii=False, indent=4)
                    
                    print(f"Progresso: {processados_agora}/{total_pendentes} contatos pendentes processados")
                else:
                    # Se falhou, coloca o contato de volta na lista
                    contatos_pendentes.append(cliente)
                
                time.sleep(1)
                
            except Exception as e:
                print(f"Erro ao processar contato: {str(e)}")
                print("Tentando continuar com o próximo contato...")
                time.sleep(3)
                continue
        
        print("\nProcessamento dos contatos pendentes concluído!")
        print(f"Total de contatos processados nesta sessão: {processados_agora}")
        
    except Exception as e:
        print(f"Erro principal: {str(e)}")
    
    finally:
        print("Fechando o navegador...")
        driver.quit()

if __name__ == "__main__":
    processar_pendentes() 