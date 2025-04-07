import json
from collections import defaultdict
import os
from datetime import datetime

def analisar_dados_completos():
    print("=== ANÁLISE COMPLETA DOS DADOS ===\n")
    
    # 1. Verificar arquivo de transportadoras
    print("1. Verificando arquivo de transportadoras...")
    try:
        with open('transportadoras_organizadas.json', 'r', encoding='utf-8') as file:
            transportadoras = json.load(file)
            print("✓ Arquivo de transportadoras encontrado")
    except FileNotFoundError:
        print("✗ Arquivo transportadoras_organizadas.json não encontrado!")
        return
    except json.JSONDecodeError:
        print("✗ Erro ao ler arquivo de transportadoras - JSON inválido!")
        return

    # 2. Verificar arquivo de progresso
    print("\n2. Verificando arquivo de progresso...")
    processados = set()
    try:
        with open('progresso_cadastro.json', 'r', encoding='utf-8') as file:
            processados = set(json.load(file))
            print("✓ Arquivo de progresso encontrado")
    except FileNotFoundError:
        print("✗ Arquivo progresso_cadastro.json não encontrado!")
    except json.JSONDecodeError:
        print("✗ Erro ao ler arquivo de progresso - JSON inválido!")

    # 3. Análise detalhada dos dados
    print("\n3. Analisando dados...")
    
    # Contadores e estruturas de dados
    total_transportadoras = 0
    total_clientes = 0
    clientes_por_transportadora = defaultdict(int)
    numeros_duplicados = defaultdict(list)
    todos_clientes = []
    
    # Analisar transportadoras e clientes
    for transportadora in transportadoras:
        total_transportadoras += 1
        nome_transportadora = transportadora.get('nome', 'Nome não disponível')
        
        if 'clientes' in transportadora and transportadora['clientes']:
            for cliente in transportadora['clientes']:
                total_clientes += 1
                clientes_por_transportadora[nome_transportadora] += 1
                
                # Adicionar informação da transportadora ao cliente
                cliente['transportadora'] = nome_transportadora
                todos_clientes.append(cliente)
                
                # Verificar duplicatas
                numero = f"{cliente['ddd']}{cliente['telefone']}"
                numeros_duplicados[numero].append({
                    'nome': cliente['nome'],
                    'transportadora': nome_transportadora
                })

    # 4. Relatório detalhado
    print("\n=== RELATÓRIO DETALHADO ===")
    print(f"\nTotal de transportadoras: {total_transportadoras}")
    print(f"Total de clientes: {total_clientes}")
    print(f"Total de números processados: {len(processados)}")
    print(f"Total de números pendentes: {total_clientes - len(processados)}")

    # 5. Verificar duplicatas
    print("\nVerificando números duplicados...")
    duplicatas_encontradas = False
    for numero, ocorrencias in numeros_duplicados.items():
        if len(ocorrencias) > 1:
            if not duplicatas_encontradas:
                print("\nNúmeros duplicados encontrados:")
                duplicatas_encontradas = True
            print(f"\nNúmero: {numero}")
            for ocorrencia in ocorrencias:
                print(f"- Cliente: {ocorrencia['nome']}")
                print(f"  Transportadora: {ocorrencia['transportadora']}")

    if not duplicatas_encontradas:
        print("✓ Nenhum número duplicado encontrado")

    # 6. Distribuição por transportadora
    print("\nDistribuição de clientes por transportadora:")
    for transportadora, quantidade in clientes_por_transportadora.items():
        print(f"- {transportadora}: {quantidade} clientes")

    # 7. Análise dos números processados
    print("\nAnálise dos números processados:")
    numeros_processados = []
    numeros_pendentes = []
    
    for cliente in todos_clientes:
        numero = f"{cliente['ddd']}{cliente['telefone']}"
        if numero in processados:
            numeros_processados.append(cliente)
        else:
            numeros_pendentes.append(cliente)

    # 8. Salvar análise em arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    relatorio = {
        "data_analise": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_transportadoras": total_transportadoras,
        "total_clientes": total_clientes,
        "total_processados": len(processados),
        "total_pendentes": len(numeros_pendentes),
        "ultimos_processados": numeros_processados[-5:] if numeros_processados else [],
        "pendentes": numeros_pendentes
    }

    nome_arquivo = f'analise_dados_{timestamp}.json'
    with open(nome_arquivo, 'w', encoding='utf-8') as file:
        json.dump(relatorio, file, ensure_ascii=False, indent=4)

    print(f"\nRelatório completo salvo em: {nome_arquivo}")

    # 9. Mostrar últimos processados e próximos pendentes
    print("\nÚltimos 5 números processados:")
    for cliente in numeros_processados[-5:]:
        print(f"- {cliente['nome']} (DDD: {cliente['ddd']}, Tel: {cliente['telefone']})")
        print(f"  Transportadora: {cliente['transportadora']}")

    print("\nPróximos números pendentes:")
    for cliente in numeros_pendentes[:5]:
        print(f"- {cliente['nome']} (DDD: {cliente['ddd']}, Tel: {cliente['telefone']})")
        print(f"  Transportadora: {cliente['transportadora']}")

    if numeros_pendentes:
        print(f"\nAinda restam {len(numeros_pendentes)} números para processar")
    else:
        print("\n✓ Todos os números foram processados!")

if __name__ == "__main__":
    analisar_dados_completos() 