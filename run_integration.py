import os
import subprocess

# Caminho para o main.py
frontend_main = os.path.join("app", "frontend", "main_integration.py")

# Executa o Streamlit
subprocess.run(["streamlit", "run", frontend_main])
