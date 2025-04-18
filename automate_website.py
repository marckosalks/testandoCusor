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

def registrar_numero_sem_whatsapp(cliente):
    """Registra números que não possuem WhatsApp em um arquivo JSON"""
    arquivo_sem_whatsapp = 'numeros_sem_whatsapp.json'
    dados = []
    
    # Verifica se o arquivo já existe
    if os.path.exists(arquivo_sem_whatsapp):
        with open(arquivo_sem_whatsapp, 'r', encoding='utf-8') as file:
            try:
                dados = json.load(file)
            except json.JSONDecodeError:
                dados = []
    
    # Adiciona o novo número à lista
    novo_registro = {
        'nome': cliente['nome'],
        'ddd': cliente['ddd'],
        'telefone': cliente['telefone'],
        'data_verificacao': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Verifica se o número já está registrado
    if not any(reg['telefone'] == cliente['telefone'] for reg in dados):
        dados.append(novo_registro)
        
        # Salva a lista atualizada
        with open(arquivo_sem_whatsapp, 'w', encoding='utf-8') as file:
            json.dump(dados, file, ensure_ascii=False, indent=4)
        print(f"Número {cliente['ddd']}{cliente['telefone']} registrado como sem WhatsApp")

def registrar_numero_ja_cadastrado(cliente, etiqueta_existente):
    """Registra números que já estão cadastrados com outras etiquetas"""
    arquivo_ja_cadastrados = 'numeros_ja_cadastrados.json'
    dados = []
    
    # Verifica se o arquivo já existe
    if os.path.exists(arquivo_ja_cadastrados):
        with open(arquivo_ja_cadastrados, 'r', encoding='utf-8') as file:
            try:
                dados = json.load(file)
            except json.JSONDecodeError:
                dados = []
    
    # Adiciona o novo registro
    novo_registro = {
        'nome': cliente['nome'],
        'ddd': cliente['ddd'],
        'telefone': cliente['telefone'],
        'etiqueta_existente': etiqueta_existente,
        'data_verificacao': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Verifica se o número já está registrado
    if not any(reg['telefone'] == cliente['telefone'] for reg in dados):
        dados.append(novo_registro)
        
        # Salva a lista atualizada
        with open(arquivo_ja_cadastrados, 'w', encoding='utf-8') as file:
            json.dump(dados, file, ensure_ascii=False, indent=4)
        print(f"Número {cliente['ddd']}{cliente['telefone']} registrado como já cadastrado com etiqueta: {etiqueta_existente}")

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

def obter_proximo_cliente(transportadoras, processados):
    """Função para obter o próximo cliente não processado do JSON"""
    for transportadora in transportadoras:
        if 'clientes' in transportadora and transportadora['clientes']:
            for cliente in transportadora['clientes']:
                cliente_id = f"{cliente['ddd']}{cliente['telefone']}"
                if cliente_id not in processados:
                    return cliente
    return None

def login_website():
    # Configurar opções do Chrome
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    
    # Inicializar o driver do Chrome
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("Abrindo o site...")
        driver.get("https://new.bitsac.com.br/")
        time.sleep(3)
        
        # Login no site
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

        # Ler arquivo de progresso se existir
        processados = set()
        if os.path.exists('progresso_cadastro.json'):
            with open('progresso_cadastro.json', 'r', encoding='utf-8') as file:
                processados = set(json.load(file))

        # Ler o arquivo de transportadoras
        with open('transportadoras_organizadas.json', 'r', encoding='utf-8') as file:
            transportadoras = json.load(file)

        total_processados = len(processados)
        total_clientes = sum(len(t.get('clientes', [])) for t in transportadoras)
        
        print(f"\nIniciando processamento de {total_clientes} contatos...")
        print(f"Já processados anteriormente: {total_processados}")
        
        ultimo_modal_processado = None
        
        while True:  # Loop infinito para continuar processando
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
                
                # Obter próximo cliente não processado
                proximo_cliente = obter_proximo_cliente(transportadoras, processados)
                
                if proximo_cliente:
                    print(f"\nProcessando cliente: {proximo_cliente['nome']} (DDD: {proximo_cliente['ddd']})")
                    
                    if processar_contato(driver, wait, proximo_cliente):
                        cliente_id = f"{proximo_cliente['ddd']}{proximo_cliente['telefone']}"
                        processados.add(cliente_id)
                        
                        # Salvar progresso
                        with open('progresso_cadastro.json', 'w', encoding='utf-8') as file:
                            json.dump(list(processados), file)
                        
                        total_processados += 1
                        print(f"Progresso: {total_processados}/{total_clientes} contatos processados")
                else:
                    print("\nTodos os contatos foram processados!")
                    break
                
                time.sleep(1)
                
            except Exception as e:
                print(f"Erro ao processar contato: {str(e)}")
                print("Tentando continuar com o próximo contato...")
                time.sleep(3)
                continue
        
        print("\nProcessamento concluído!")
        print(f"Total de contatos processados: {total_processados}")
        
    except Exception as e:
        print(f"Erro principal: {str(e)}")
    
    finally:
        print("Fechando o navegador...")
        driver.quit()

if __name__ == "__main__":
    login_website() 