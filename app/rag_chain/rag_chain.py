import os
import sys
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.models.rag_chain_builder import load_all_documents, llm, embedding
from app.models.prompt_sofia import SOFIA_PROMPT

# Configs
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX")


def build_rag_chain(llm, prompt_template):
    # Carrega e prepara os documentos
    documents = load_all_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    # Indexa no Pinecone (ou carrega índice já existente, se preferir)
    vectorstore = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embedding,
        index_name=PINECONE_INDEX_NAME,
        namespace="default"
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Cria a cadeia RAG
    doc_chain = create_stuff_documents_chain(llm,SOFIA_PROMPT)
    rag_chain = create_retrieval_chain(retriever, doc_chain)

    return rag_chain


# ask_sofia.py
def ask_sofia(question: str, rag_chain) -> str:
    response = rag_chain.invoke({"input": question})
    return response.get("answer", "Sem resposta.")


if __name__ == "__main__":
    
    print("🔍 Teste direto do RAG:")
    question = input("❓ Faça uma pergunta para a SofiA: ")
    resposta = ask_sofia(question, rag_chain= build_rag_chain(llm, SOFIA_PROMPT))
    print("\n💡 Resposta da SofiA:\n")
    print(resposta)