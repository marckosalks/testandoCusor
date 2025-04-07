import json

def analisar_progresso():
    # Carregar contatos processados
    processados = set()
    try:
        with open('progresso_cadastro.json', 'r', encoding='utf-8') as file:
            processados = set(json.load(file))
    except FileNotFoundError:
        print("Arquivo de progresso não encontrado!")
        return

    # Carregar todos os contatos
    try:
        with open('transportadoras_organizadas.json', 'r', encoding='utf-8') as file:
            transportadoras = json.load(file)
    except FileNotFoundError:
        print("Arquivo de transportadoras não encontrado!")
        return

    # Lista para armazenar todos os contatos
    todos_contatos = []
    
    # Coletar todos os contatos com informações da transportadora
    for transportadora in transportadoras:
        if 'clientes' in transportadora and transportadora['clientes']:
            for cliente in transportadora['clientes']:
                cliente['transportadora'] = transportadora.get('nome', 'Nome não disponível')
                todos_contatos.append(cliente)

    # Separar contatos processados e pendentes
    contatos_processados = []
    contatos_pendentes = []

    for cliente in todos_contatos:
        cliente_id = f"{cliente['ddd']}{cliente['telefone']}"
        if cliente_id in processados:
            contatos_processados.append(cliente)
        else:
            contatos_pendentes.append(cliente)

    # Imprimir resultados
    print(f"\nTotal de contatos: {len(todos_contatos)}")
    print(f"Contatos processados: {len(contatos_processados)}")
    print(f"Contatos pendentes: {len(contatos_pendentes)}")

    print("\nÚltimos 5 contatos processados:")
    for i, cliente in enumerate(contatos_processados[-5:], 1):
        print(f"{i}. Nome: {cliente['nome']}")
        print(f"   DDD: {cliente['ddd']}")
        print(f"   Telefone: {cliente['telefone']}")
        print(f"   Transportadora: {cliente['transportadora']}\n")

    print("\nContatos pendentes:")
    for i, cliente in enumerate(contatos_pendentes, 1):
        print(f"{i}. Nome: {cliente['nome']}")
        print(f"   DDD: {cliente['ddd']}")
        print(f"   Telefone: {cliente['telefone']}")
        print(f"   Transportadora: {cliente['transportadora']}\n")

    # Salvar contatos pendentes em um arquivo separado
    with open('contatos_pendentes.json', 'w', encoding='utf-8') as file:
        json.dump(contatos_pendentes, file, ensure_ascii=False, indent=4)
    print("\nContatos pendentes foram salvos em 'contatos_pendentes.json'")

if __name__ == "__main__":
    analisar_progresso() 