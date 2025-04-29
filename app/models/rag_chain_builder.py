import os
import sys
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_openai import ChatOpenAI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.utils.read_drive import read_drive_folder
from app.models.prompt_sofia import SOFIA_PROMPT

load_dotenv()

# Configs
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX")

# Embeddings com Cohere
embedding = CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=COHERE_API_KEY)

# Chat LLM (OpenAI)
llm_openai = ChatOpenAI(
    temperature=0.1,
    model_name="gpt-3.5-turbo",
    open_api_key=OPENAI_API_KEY
)

# Chat LLM (Groq)
llm = ChatGroq(
    temperature=0.1,
    model_name="llama3-8b-8192",
    groq_api_key=GROQ_API_KEY
)


def load_all_documents(max_tokens: int | None = None) -> list[Document]:
    """
    Lê todos os arquivos .pdf e .csv do Google Drive e retorna uma lista com 1 Document.

    Args:
        max_tokens (int | None): Limite de caracteres a serem lidos. Se None, lê tudo.

    Returns:
        list[Document]: Lista com o conteúdo consolidado em um único Document.
    """
    drive_link = os.getenv("GOOGLE_DRIVE_FILE_LINK")
    
    if not drive_link:
        raise ValueError("O link do Google Drive não foi definido nas variáveis de ambiente.")
    
    drive_text = read_drive_folder(drive_link)

    if max_tokens is not None and len(drive_text) > max_tokens:
        drive_text = drive_text[:max_tokens]

    return [Document(page_content=drive_text)]

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

    # Cria pipeline RAG moderno
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    doc_chain = create_stuff_documents_chain(llm, SOFIA_PROMPT)
    rag_chain = create_retrieval_chain(retriever, doc_chain)

    # Executa
    response = rag_chain.invoke({"input": question})
    return response.get("answer", "Sem resposta.")

if __name__ == "__main__":
    print("🔍 Teste direto do RAG:")
    question = input("❓ Faça uma pergunta para a SofiA: ")
    resposta = ask_sofia_with_rag(question)
    print("\n💡 Resposta da SofiA:\n")
    print(resposta)