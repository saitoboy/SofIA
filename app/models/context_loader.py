import pandas as pd
from app.utils.file_reader import read_csv
from PyPDF2 import PdfReader
import os

def load_context_from_csv(file_path: str, for_langchain: bool = False) -> str:
    """
    Carrega dados de um arquivo CSV e os transforma em um contexto utilizável para o chatbot.
    
    Args:
        file_path (str): Caminho completo do arquivo CSV.
        for_langchain (bool): Se True, formata o contexto para uso no LangChain.
    
    Returns:
        str: Contexto formatado como uma string.
    """
    try:
        print("📂 Lendo o arquivo CSV...")  # Log amigável
        # Lê o arquivo CSV usando o file_reader
        data = read_csv(file_path)
        
        print("✅ Arquivo CSV lido com sucesso!")  # Log amigável
        
        if for_langchain:
            print("📜 Formatando os dados para LangChain...")  # Log amigável
            # Formata os dados como texto simples para LangChain
            context = ""
            for index, row in data.iterrows():
                context += ", ".join([f"{col}: {row[col]}" for col in data.columns if pd.notna(row[col])]) + "\n"
        else:
            print("📊 Formatando os dados em formato de tabela...")  # Log amigável
            # Usa tabulate para formatar o DataFrame como uma tabela
            from tabulate import tabulate
            context = tabulate(data, headers="keys", tablefmt="grid")
        
        print("🎉 Contexto formatado com sucesso!")  # Log amigável
        return context
    except Exception as e:
        print(f"❌ Erro ao carregar o contexto do CSV: {e}")  # Log amigável
        raise ValueError(f"Erro ao carregar o contexto do CSV: {e}")

def load_context_from_pdf(file_path: str) -> str:
    """
    Extrai texto de um arquivo PDF.

    Args:
        file_path (str): Caminho completo do arquivo PDF.

    Returns:
        str: Texto extraído do PDF.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise ValueError(f"Erro ao ler o PDF: {e}")

def load_default_pdf_context(data_folder: str = r"d:\SofIA\app\data") -> str:
    """
    Verifica se o arquivo PDF padrão existe na pasta de dados e carrega seu conteúdo.

    Args:
        data_folder (str): Caminho para a pasta de dados.

    Returns:
        str: Texto extraído do PDF, ou uma mensagem de erro se o arquivo não for encontrado.
    """
    pdf_file = os.path.join(data_folder, "institucional.pdf")
    print(f"🔍 Verificando o arquivo PDF no caminho: {pdf_file}")  # Log para depuração
    if os.path.exists(pdf_file):
        print(f"📂 Arquivo PDF encontrado: {pdf_file}")
        return load_context_from_pdf(pdf_file)
    else:
        print(f"❌ Arquivo PDF não encontrado no caminho: {pdf_file}")  # Log para depuração
        raise FileNotFoundError(f"Arquivo PDF institucional não encontrado em {data_folder}.")