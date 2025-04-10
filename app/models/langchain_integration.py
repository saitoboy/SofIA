import requests
import json
from dotenv import load_dotenv
import os
from app.models.context_loader import load_context_from_csv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def ask_gemini(context: str, question: str) -> str:
    """
    Envia uma pergunta para a API Gemini com base no contexto fornecido.
    
    Args:
        context (str): O contexto a ser enviado para a API.
        question (str): A pergunta do usuário.
    
    Returns:
        str: A resposta da API Gemini.
    """
    # Configura a URL e o cabeçalho da API Gemini
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}"
    headers = {
        "Content-Type": "application/json"
    }
    
    # Define o payload com o contexto e a pergunta
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "Você é Sofia, uma assistente virtual inteligente criada para ajudar os usuários "
                            "a entenderem dados sobre concessões de rodovias no Brasil. Você é educada, clara e objetiva.\n\n"
                            f"Com base no seguinte contexto:\n\n{context}\n\n"
                            f"Responda à seguinte pergunta:\n\n{question}"
                        )
                    }
                ]
            }
        ]
    }
    
    # Faz a chamada à API Gemini
    print("🌐 Enviando solicitação para a API Gemini...")
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Verifica a resposta
    if response.status_code == 200:
        print("✅ Resposta recebida com sucesso!")
        result = response.json()
        # Acessa o texto da resposta no campo correto
        output = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Sem resposta")
        return output
    else:
        print(f"❌ Erro ao chamar a API Gemini: {response.status_code}")
        print(response.text)
        return "Erro ao obter resposta da API."

def process_with_gemini(file_path: str):
    """
    Processa o contexto do CSV e permite que o usuário faça perguntas dinâmicas.
    
    Args:
        file_path (str): Caminho completo do arquivo CSV.
    """
    print("🚀 Iniciando integração com a API Gemini...")  # Log amigável
    
    # Carrega o contexto do CSV
    context = load_context_from_csv(file_path, for_langchain=True)
    print("📜 Contexto carregado para a API Gemini:")
    print(context[:500])  # Exibe os primeiros 500 caracteres do contexto
    
    while True:
        # Pergunta do usuário
        question = input("❓ Faça sua pergunta (ou digite 'sair' para encerrar): ")
        if question.lower() == "sair":
            print("👋 Encerrando o programa. Até mais!")
            break
        
        # Envia a pergunta para a API Gemini
        response = ask_gemini(context, question)
        print("💡 Resposta da Sofia:")
        print(response)

# Teste a integração
if __name__ == "__main__":
    file_path = r"d:\SofIA\app\data\data2.csv"  # Substitua pelo caminho correto do seu arquivo CSV
    process_with_gemini(file_path)