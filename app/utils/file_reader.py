import pandas as pd

def read_csv(file_path: str) -> pd.DataFrame:
    """
    Lê um arquivo CSV e retorna um DataFrame do pandas.
    
    Args:
        file_path (str): Caminho completo do arquivo CSV.
    
    Returns:
        pd.DataFrame: Dados do arquivo CSV.
    """
    try:
        # Especifica a codificação como ISO-8859-1 para evitar erros de decodificação
        data = pd.read_csv(file_path, encoding="ISO-8859-1", on_bad_lines='skip')
        return data
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo CSV: {e}")