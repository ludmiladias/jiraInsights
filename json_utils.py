import json
import re

def parse_to_json(string_with_json):
    json_pattern = re.compile(r'```json\n(.*?)```', re.DOTALL)
    match = json_pattern.search(string_with_json)
    if match:
        json_content = match.group(1).strip()
        
        try:
            return json.loads(json_content)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar o JSON: {e}")
            print("Conteúdo recebido:", json_content)
            return None
    else:
        print("Nenhum bloco de código JSON encontrado.")
        return None
