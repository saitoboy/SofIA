import requests
import json
from dotenv import load_dotenv
import os
from app.models.context_loader import load_context_from_csv
from app.models.prompt_sofia import SOFIA_PROMPT

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def ask_groq(context: str, question: str) -> str:
    """
    Envia uma pergunta para a API Groq com base no contexto fornecido e na identidade da Sofia.
    
    Args:
        context (str): O contexto a ser enviado para a API.
        question (str): A pergunta do usuário.
    
    Returns:
        str: A resposta da API Groq.
    """
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"
    }

    # Define a identidade e o comportamento da Sofia
    sofia_identity = SOFIA_PROMPT

    payload = {
        "model": "llama3-8b-8192",  # Ou outro modelo suportado pela Groq
        "messages": [
            {"role": "system", "content": "Você é uma assistente útil."},
            {"role": "user", "content": sofia_identity.format(context=context, question=question)}
        ],
        "temperature": 0.7
    }

    print("🌐 Enviando solicitação para a API Groq...")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("✅ Resposta recebida com sucesso!")
        result = response.json()
        output = result.get("choices", [{}])[0].get("message", {}).get("content", "Sem resposta")
        return output
    else:
        print(f"❌ Erro ao chamar a API Groq: {response.status_code}")
        print(response.text)
        return "Erro ao obter resposta da API."
    