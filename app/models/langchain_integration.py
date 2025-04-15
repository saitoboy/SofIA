import requests
import json
from dotenv import load_dotenv
import os
from app.models.context_loader import load_context_from_csv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def ask_gemini(context: str, question: str) -> str:
    """
    Envia uma pergunta para a API Gemini com base no contexto fornecido e na identidade da Sofia.
    
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
    
    # Define o payload com o contexto, a pergunta e a identidade da Sofia
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": sofia_identity.format(context=context, question=question)
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