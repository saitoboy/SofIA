import os
import subprocess

# Caminho para o main.py
frontend_main_rag = os.path.join("app", "frontend", "main_rag.py")

# Executa o Streamlit
subprocess.run(["streamlit", "run", frontend_main_rag])
