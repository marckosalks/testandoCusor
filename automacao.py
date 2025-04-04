import time
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Configuração do arquivo de log
log_file = f"log_busca_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def write_to_log(message):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")

# Obtém o diretório onde o script está rodando


# 🔹 Configuração para acessar o Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
caminho_json = os.path.join(os.getcwd(), "automacaoplanilhhabling.json")

try:
    creds = ServiceAccountCredentials.from_json_keyfile_name(caminho_json, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("19_Pt5ykYPB4UnwHiolo4l1FK8Q8tweZi7wbEqrPnW3U").sheet1
    nomes = sheet.col_values(1)  # Pegar todos os valores
    
    print("\n📋 Lista de todos os elementos na planilha:")
    for i, nome in enumerate(nomes):
        print(f"Linha {i+1}: {nome}")
    
    # Perguntar ao usuário por qual elemento começar
    primeiro_elemento = input("\n➡️ Digite o número da linha por onde quer começar (ou pressione ENTER para começar do início): ")
    
    if primeiro_elemento.strip():
        try:
            indice_inicio = int(primeiro_elemento) - 1  # Converter para índice base 0
            if 0 <= indice_inicio < len(nomes):
                nomes = nomes[indice_inicio:]
                print(f"✅ Começando pela linha {indice_inicio + 1}: {nomes[0]}")
            else:
                print("⚠️ Número de linha inválido. Começando do início.")
        except ValueError:
            print("⚠️ Entrada inválida. Começando do início.")
    else:
        print("✅ Começando do início da planilha")
    
    print(f"\n📊 Total de elementos a processar: {len(nomes)}")
    print(f"🏁 Primeiro elemento: {nomes[0]}")
    input("\n⏸️ Pressione ENTER para começar a automação...")
except Exception as e:
    print(f"❌ Erro ao conectar com a planilha. Detalhes do erro: {str(e)}")
    import traceback
    print("Stack trace completo:")
    print(traceback.format_exc())
    exit()

# 🔹 Configuração do Selenium
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://tracken.app.br/tracken/#")
    print("⏳ Aguardando página carregar...")
    time.sleep(15)  # Aumentado de 10 para 15 segundos
    
    # Verifica se precisa fazer login
    try:
        login_field = driver.find_element(By.ID, "username")
        if login_field:
            print("🔐 Por favor, faça o login manualmente e pressione ENTER quando estiver pronto...")
            input()
    except:
        print("✅ Já está logado ou login não é necessário")

    # 🔹 Configurar o filtro "Nome Fantasia" uma única vez
    print("⏳ Configurando filtro 'Nome Fantasia'...")
    dropdown_button = WebDriverWait(driver, 15).until(  # Aumentado de 10 para 15 segundos
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-id='cli_vbuscaf']"))
    )
    dropdown_button.click()
    time.sleep(2)  # Aumentado de 1 para 2 segundos

    opcoes = driver.find_elements(By.CSS_SELECTOR, ".dropdown-menu li")
    for opcao in opcoes:
        if opcao.text.strip() == "Nome Fantasia":
            opcao.click()
            break
    time.sleep(2)  # Aumentado de 1 para 2 segundos
    print("✅ Filtro 'Nome Fantasia' configurado com sucesso!")

    # Para cada nome na planilha
    for nome in nomes:
        try:
            print(f"\n🔍 Processando: {nome}")
            write_to_log(f"Processando: {nome}")
            time.sleep(3)  # Aumentado de 2 para 3 segundos

            # Espera explícita pelo campo de busca
            campo_pesquisa = WebDriverWait(driver, 15).until(  # Aumentado de 10 para 15 segundos
                EC.presence_of_element_located((By.ID, "cli_vbuscav"))
            )
            campo_pesquisa.clear()
            campo_pesquisa.send_keys(nome)

            time.sleep(2)  # Aumentado de 1 para 2 segundos

            # 🔹 Clicar no botão de pesquisa
            botao_pesquisa = driver.find_element(By.ID, "btsearch")
            botao_pesquisa.click()

            # Aguarda os resultados carregarem
            time.sleep(5)  # Aumentado de 3 para 5 segundos

            try:
                # 🔹 Encontrar a tabela e extrair informações
                tbody = driver.find_element(By.CSS_SELECTOR, "tbody")
                linha = tbody.find_element(By.TAG_NAME, "tr")
                
                # Extrair informações das células
                colunas = linha.find_elements(By.TAG_NAME, "td")
                
                print("\n🔍 DEBUG - Conteúdo de todas as colunas:")
                for i, coluna in enumerate(colunas):
                    print(f"Coluna {i}: [{coluna.text}]")
                
                # Criar dicionário com as informações
                dados = {
                    "Sequencia": colunas[0].text,
                    "ID": colunas[1].text,
                    "Codigo": colunas[2].text,
                    "Nome": colunas[3].text,
                    "Nome_Fantasia": colunas[4].text,
                    "CNPJ": colunas[5].text,
                    "CEP": colunas[7].text,
                    "Telefone": colunas[6].text,
                    "Data_Validade": colunas[11].text,
                    "Ultima_Atualizacao": colunas[12].text,
                    "Token": colunas[13].text
                }
                
                # Salvar informações no log
                write_to_log(f"{nome} - {dados['Telefone'] if dados['Telefone'] and dados['Telefone'].strip() else 'Telefone não encontrado'}")
                write_to_log("-" * 50)  # Separador entre registros

            except Exception as e:
                print(f"⚠️ Erro ao extrair dados da tabela: {str(e)}")
                write_to_log(f"{nome} - Loja não encontrada")
                write_to_log("-" * 50)  # Separador entre registros

            time.sleep(3)  # Espera os resultados carregarem

        except Exception as e:
            print(f"⚠️ Erro ao processar '{nome}': {e}")
            write_to_log(f"Erro ao processar '{nome}': {e}")
            write_to_log("-" * 50)  # Separador entre registros

    print("✅ Automação finalizada!")
    write_to_log("Automação finalizada!")
except Exception as e:
    print(f"❌ Erro ao abrir o navegador: {e}")
finally:
    driver.quit()
