from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from app.models.context_loader import load_context_from_csv

def process_with_langchain(file_path: str):
    """
    Processa o contexto do CSV e envia para o LangChain.
    
    Args:
        file_path (str): Caminho completo do arquivo CSV.
    """
    print("🚀 Iniciando integração com LangChain...")  # Log amigável
    
    # Carrega o contexto do CSV
    context = load_context_from_csv(file_path, for_langchain=True)
    print("📜 Contexto carregado para LangChain:")
    print(context[:500])  # Exibe os primeiros 500 caracteres do contexto
    
    # Define o modelo LLM (substitua pela sua chave de API do OpenAI)
    llm = OpenAI(temperature=0.7, openai_api_key="SUA_CHAVE_API_AQUI")
    
    # Define o prompt para o LangChain
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="Com base no seguinte contexto:\n\n{context}\n\nResponda à seguinte pergunta:\n\n{question}"
    )
    
    # Cria a cadeia do LangChain
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Pergunta de exemplo
    question = "Qual é o município com o maior valor de Cod_IBGE?"
    print(f"❓ Pergunta: {question}")
    
    # Executa a cadeia com o contexto e a pergunta
    response = chain.run({"context": context, "question": question})
    print("💡 Resposta do LangChain:")
    print(response)

# Teste a integração
if __name__ == "__main__":
    file_path = r"d:\SofIA\app\data\data2.csv"  # Substitua pelo caminho correto do seu arquivo CSV
    process_with_langchain(file_path)