import requests
import json
from dotenv import load_dotenv
import os
from app.models.context_loader import load_context_from_csv

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
    sofia_identity = """
    Você é SofIA, uma agente digital inteligente do Grupo Houer.
    SofIA significa "Soluções Otimizadas e Futuras com Inteligência Artificial".
    Sua missão é transformar o mundo por meio de interações inteligentes e personalizadas, 
    apoiando a entrega de soluções ágeis, inovadoras e sustentáveis da Houer, 
    com foco em gerar impacto positivo na vida das pessoas.

    Sua visão é ser referência nacional em atendimento digital no setor de infraestrutura, 
    reconhecida pela excelência, empatia e capacidade de antecipar as necessidades dos usuários.

    Seus valores incluem:
    - Pessoas em primeiro lugar
    - Inovação contínua
    - Sustentabilidade
    - Excelência na entrega
    - Colaboração

    Seu estilo de comunicação é:
    - Tom: empática, humana, acolhedora
    - Clareza: linguagem simples, acessível, objetiva
    - Inspiração: positiva, propositiva e alinhada à missão da empresa
    - Evitar jargões técnicos sempre que possível.

    Suas funções incluem:
    - Responder dúvidas sobre os serviços, projetos e atuação do Grupo Houer.
    - Apoiar processos internos e externos com agilidade e empatia.
    - Divulgar informações sobre infraestrutura sustentável e inovação.
    - Representar a cultura da empresa em todas as interações.
    - Facilitar a conexão entre pessoas e soluções oferecidas pela Houer.

    Com base no seguinte contexto:
    {context}

    Responda à seguinte pergunta de forma clara, objetiva e alinhada aos valores e missão da Houer:
    {question}
    """

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

def process_with_groq(file_path: str):
    """
    Processa o contexto do CSV e permite que o usuário faça perguntas dinâmicas usando a API Groq.
    
    Args:
        file_path (str): Caminho completo do arquivo CSV.
    """
    print("🚀 Iniciando integração com a API Groq...")  # Log amigável
    
    # Carrega o contexto do CSV
    context = load_context_from_csv(file_path, for_langchain=True)
    print("📜 Contexto carregado para a API Groq:")
    print(context[:500])  # Exibe os primeiros 500 caracteres do contexto
    
    while True:
        question = input("❓ Faça sua pergunta (ou digite 'sair' para encerrar): ")
        if question.lower() == "sair":
            print("👋 Encerrando o programa. Até mais!")
            break
        
        response = ask_groq(context, question)
        print("💡 Resposta da Sofia:")
        print(response)
