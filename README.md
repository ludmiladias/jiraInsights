## 🎯 Visão Geral
Uma aplicação em Python que utiliza **inteligência artificial e engenharia de prompt** para mapear rapidamente bugs em aplicações complexas. Ela se conecta ao Jira, coleta os bugs atualizados nos últimos XX dias e analisa os títulos das tasks para identificar:  

- O **módulo principal** impactado  
- A **possível causa do bug**, resumida em até duas palavras  
- Retorna os resultados em **JSON**, prontos para análise automática  

## Funcionalidades principais

- Conexão automática com o Jira  
- Classificação inteligente de bugs por módulo e motivo  
- Geração de relatórios em JSON para fácil integração  
- Código aberto, pronto para adaptação e colaboração da comunidade  

## Benefícios

- Identifica rapidamente módulos críticos  
- Prioriza correções estratégicas  
- Detecta padrões recorrentes de bugs  
- Reduz retrabalho e agiliza a tomada de decisão

## 📦 Dependências

Instale os pacotes necessários com:

```bash
pip install jira wordcloud matplotlib nltk scikit-learn python-dotenv openai google-genai
```

## ⚙️ Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
REQUESTER_TOKEN=JIRA_SERVER="https://suaempresa.atlassian.net"
JIRA_USER="seu.email@empresa.com"
JIRA_TOKEN="seu_token_api"
JIRA_PROJECT_KEY="key_do_projeto"
JIRA_UPDATED=qtd_dias_analisados (-45 para ultimos 45, por exemplo. )

AI_CLIENT = iforme o tipo: gemini / chatgpt
AI_REQUESTER_TOKEN=Seu Token
AI_MODEL = Modelo utilizado
AI_URL= Base URL da sua IA (se não tiver deixar como "")
```

## ▶️ Uso

Execute o script principal:

```bash
python bug_insights_wordscloud.py
```
