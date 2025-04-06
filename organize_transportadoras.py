import re

def clean_name(name):
    # Remove newlines and clean duplicate names
    name = name.replace('\n', ' ')
    # Remove duplicate words
    words = name.split()
    unique_words = []
    for word in words:
        if word not in unique_words:
            unique_words.append(word)
    return ' '.join(unique_words)

def extract_phone_info(phone_str):
    # Extract DDD and phone number
    phone_pattern = r'(\d{2})?\s*(\d{4,5}[-.]?\d{4})'
    match = re.search(phone_pattern, phone_str)
    if match:
        ddd = match.group(1) or '11'  # Default to 11 if no DDD found
        phone = match.group(2).replace('-', '').replace('.', '')
        return ddd, phone
    return '11', ''  # Default to 11 if no phone number found

def parse_transportadoras(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Split content by transportadora sections
    sections = re.split(r'Transportadora\s+', content)
    transportadoras = []
    
    for section in sections[1:]:  # Skip first empty section
        if not section.strip():
            continue
            
        # Extract transportadora name
        transportadora_name = clean_name(section.split('\n')[0].strip())
        
        # Find all client entries
        client_entries = re.findall(r'Processando:\s*(.*?)\s*-\s*(.*?)(?=\n-{50}|\Z)', section, re.DOTALL)
        
        clients = []
        for client_name, phone_info in client_entries:
            client_name = clean_name(client_name.strip())
            ddd, phone = extract_phone_info(phone_info)
            clients.append({
                'nome': client_name,
                'ddd': ddd,
                'telefone': phone
            })
        
        transportadoras.append({
            'nome': transportadora_name,
            'clientes': clients
        })
    
    return transportadoras

def save_to_json(transportadoras, output_file):
    import json
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transportadoras, f, ensure_ascii=False, indent=2)

def main():
    input_file = 'Transportadoras logs.txt'
    output_file = 'transportadoras_organizadas.json'
    
    transportadoras = parse_transportadoras(input_file)
    save_to_json(transportadoras, output_file)
    print(f"Data organized and saved to {output_file}")

if __name__ == "__main__":
    main() 