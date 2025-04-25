import pandas as pd
from PyPDF2 import PdfReader
import os
from tabulate import tabulate  # Certifique-se de que o tabulate está instalado

# Caminho base para a pasta /app
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')


def read_csv(file_path: str) -> pd.DataFrame:
    try:
        # Especifica a codificação como ISO-8859-1 para evitar erros de decodificação
        data = pd.read_csv(file_path, encoding="ISO-8859-1", on_bad_lines='skip')
        return data
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo CSV: {e}")
    
def load_context_from_csv(file_path: str, for_langchain: bool = False) -> str:
    try:
        print("📂 Lendo o arquivo CSV...")
        data = pd.read_csv(file_path, encoding="latin1", on_bad_lines='skip')
        print("✅ Arquivo CSV lido com sucesso!")

        if for_langchain:
            print("📜 Formatando os dados para LangChain...")
            context = ""
            for index, row in data.iterrows():
                context += ", ".join([
                    f"{col}: {row[col]}" for col in data.columns if pd.notna(row[col])]) + "\n"
        else:
            print("📊 Formatando os dados em formato de tabela...")
            context = tabulate(data, headers="keys", tablefmt="grid")

        print("🎉 Contexto formatado com sucesso!")
        return context
    except UnicodeDecodeError as e:
        print(f"❌ Erro de codificação ao carregar o CSV: {e}")
        raise ValueError(f"Erro de codificação ao carregar o CSV: {e}")
    except Exception as e:
        print(f"❌ Erro ao carregar o contexto do CSV: {e}")
        raise ValueError(f"Erro ao carregar o contexto do CSV: {e}")

def load_all_csv_contexts(for_langchain: bool = False) -> str:
    context = ""
    print("📂 Procurando por arquivos CSV em:", DATA_DIR)
    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            file_path = os.path.join(DATA_DIR, file)
            try:
                context += load_context_from_csv(file_path, for_langchain=for_langchain) + "\n"
            except Exception as e:
                print(f"⚠️ Erro ao processar {file}: {e}")
    return context

def load_context_from_pdf(file_path: str) -> str:
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise ValueError(f"Erro ao ler o PDF: {e}")

def load_all_pdf_contexts() -> str:
    text = ""
    print("📂 Procurando por arquivos PDF em:", DATA_DIR)
    for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            file_path = os.path.join(DATA_DIR, file)
            try:
                text += load_context_from_pdf(file_path) + "\n"
            except Exception as e:
                print(f"⚠️ Erro ao processar {file}: {e}")
    return text

def load_default_pdf_context(data_folder: str = DATA_DIR) -> str:
    pdf_file = os.path.join(data_folder, "institucional.pdf")
    print(f"🔍 Verificando o arquivo PDF no caminho: {pdf_file}")
    if os.path.exists(pdf_file):
        print(f"📂 Arquivo PDF encontrado: {pdf_file}")
        return load_context_from_pdf(pdf_file)
    else:
        print(f"❌ Arquivo PDF não encontrado no caminho: {pdf_file}")
        raise FileNotFoundError(f"Arquivo PDF institucional não encontrado em {data_folder}.")
