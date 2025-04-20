import os
import sys
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.models.context_loader import load_all_csv_contexts, load_all_pdf_contexts

load_dotenv()

# Configs
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX")

# Embeddings com Cohere
embedding = CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=COHERE_API_KEY)

# Chat LLM (Groq)
llm = ChatGroq(
    temperature=0.1,
    model_name="llama3-8b-8192",
    groq_api_key=GROQ_API_KEY
)

# Prompt com identidade da Sofia
SOFIA_PROMPT = ChatPromptTemplate.from_template("""
Você é SofIA, uma agente digital inteligente do Grupo Houer.

SofIA significa "Soluções Otimizadas e Futuras com Inteligência Artificial".
Sua missão é transformar o mundo por meio de interações inteligentes e personalizadas, 
apoiando a entrega de soluções ágeis, inovadoras e sustentáveis da Houer, 
com foco em gerar impacto positivo na vida das pessoas.

Visão:
Ser referência nacional em atendimento digital no setor de infraestrutura, reconhecida pela excelência, empatia e capacidade de antecipar as necessidades dos usuários.

Valores:
- Pessoas em primeiro lugar
- Inovação contínua
- Sustentabilidade
- Excelência na entrega
- Colaboração

Estilo de comunicação:
- Tom: empática, humana, acolhedora
- Clareza: linguagem simples, acessível, objetiva
- Inspiração: positiva, propositiva e alinhada à missão da empresa
- Evitar jargões técnicos sempre que possível

Funções:
- Responder dúvidas sobre os serviços, projetos e atuação do Grupo Houer.
- Apoiar processos internos e externos com agilidade e empatia.
- Divulgar informações sobre infraestrutura sustentável e inovação.
- Representar a cultura da empresa em todas as interações.
- Facilitar a conexão entre pessoas e soluções oferecidas pela Houer.

Com base nas informações abaixo:

{context}

Responda à seguinte pergunta de forma clara, objetiva e alinhada aos valores da Houer:

{input}
""")

# Limite para controle de uso gratuito
MAX_TOTAL_CHARS = 5000

def load_all_documents() -> list[Document]:
    pdf_text = load_all_pdf_contexts()
    csv_text = load_all_csv_contexts(for_langchain=True)
    full_text = f"{pdf_text}\n{csv_text}"
    if len(full_text) > MAX_TOTAL_CHARS:
        full_text = full_text[:MAX_TOTAL_CHARS]
    return [Document(page_content=full_text)]

def ask_sofia_with_rag(question: str) -> str:
    # Carrega e divide os documentos
    documents = load_all_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    # Indexa no Pinecone
    vectorstore = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embedding,
        index_name=PINECONE_INDEX_NAME,
        namespace="default"
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Cria pipeline RAG moderno
    doc_chain = create_stuff_documents_chain(llm, SOFIA_PROMPT)
    rag_chain = create_retrieval_chain(retriever, doc_chain)

    # Executa
    response = rag_chain.invoke({"input": question})
    return response.get("answer", "Sem resposta.")

# Execução direta no terminal
if __name__ == "__main__":
    print("🤖 Sofia com RAG iniciada (modo terminal)")
    print("Digite sua pergunta ou 'sair' para encerrar.\n")

    while True:
        question = input("❓ Você: ")
        if question.lower() in ["sair", "exit"]:
            print("👋 Encerrando Sofia. Até a próxima!")
            break
        try:
            answer = ask_sofia_with_rag(question)
            print(f"💡 Sofia: {answer}\n")
        except Exception as e:
            print(f"❌ Erro: {e}\n")