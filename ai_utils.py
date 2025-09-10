import openai
from dotenv import load_dotenv
import os
from google import genai
import json_utils


load_dotenv()
AI_REQUESTER_TOKEN = os.getenv("AI_REQUESTER_TOKEN", "")
AI_MODEL = os.getenv("AI_MODEL","")
AI_URL = os.getenv("AI_URL","")
AI_CLIENT =  os.getenv("AI_CLIENT","")

# AI client configuration
def get_ai_client():
    if AI_CLIENT=="gemini":
        return genai.Client(api_key=AI_REQUESTER_TOKEN)
    else:        
        if AI_URL is None or AI_URL=="":
            return openai.OpenAI(
                api_key=AI_REQUESTER_TOKEN
            )
        return openai.OpenAI(
            api_key=AI_REQUESTER_TOKEN,      
            base_url=AI_URL
        )
    


def load_prompt_template(prompt_name):
    prompt_path = os.path.join("resources", "prompts", f"{prompt_name}.md")
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️  Arquivo de prompt não encontrado: {prompt_path}")
        return f"Erro: Template de prompt '{prompt_name}' não encontrado."
    except Exception as e:
        print(f"⚠️  Erro ao carregar prompt: {str(e)}")
        return f"Erro ao carregar template: {str(e)}"
    

def send_request_to_ai(prompt):
     if AI_CLIENT=="gemini":
        return _send_request_to_gemini(prompt)
     else:
        return _send_request_to_openai(prompt)

def _send_request_to_gemini(prompt):
    ai_client = get_ai_client()
    try:
        response = ai_client.models.generate_content(
            model=AI_MODEL, 
            contents=prompt
        )
        
        return json_utils.parse_to_json(response.text)
    except Exception as e:
        print(f"\n\033[91mErro ao enviar a requisição: {str(e)}\033[0m")
        print("Tente novamente ou verifique sua conexão e configuração da API.")
        return None

def _send_request_to_openai(prompt):
  
    ai_client = get_ai_client()
    try:
        response = ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return json_utils.parse_to_json(response.choices[0].message.content)
    except Exception as e:
        print(f"\n\033[91mErro ao enviar a requisição: {str(e)}\033[0m")
        print("Tente novamente ou verifique sua conexão e configuração da API.")
        return None
   

def generate_bug_analisys_prompt(titles):
    prompt = load_prompt_template("bug_analisys")        
    prompt += "\n\n## Títulos para Análise\n\n"
    for title in titles:
        prompt += f"#### Título: {title}\n\n"
    
    return prompt