import pandas as pd
from app.utils.file_reader import read_csv

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