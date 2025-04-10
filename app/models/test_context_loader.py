import os
import sys

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.models.context_loader import load_context_from_csv

def test_load_context():
    # Caminho correto para o arquivo CSV
    file_path = r"d:\SofIA\app\data\data2.csv"  # Atualizado para o local correto
    
    # Carrega o contexto
    try:
        context = load_context_from_csv(file_path)
        print("Contexto carregado com sucesso:")
        print(context)
    except Exception as e:
        print(f"Erro ao carregar o contexto: {e}")

if __name__ == "__main__":
    test_load_context()