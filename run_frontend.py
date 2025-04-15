import os
import subprocess

# Caminho para o main.py
frontend_main = os.path.join("app", "frontend", "main.py")

# Executa o Streamlit
subprocess.run(["streamlit", "run", frontend_main])
