#!/bin/bash


# === Nome do Projeto ===
PROJECT_NAME="SofIA"
cd D:/ || exit

# === Cria pasta e ambiente virtual ===
mkdir $PROJECT_NAME
cd $PROJECT_NAME || exit
python -m venv venv
source venv/Scripts/activate

# === Instala as dependências ===
pip install --upgrade pip 
pip install fastapi uvicorn langchain pandas python-multipart openai

# === Cria estrutura básica de projeto ===
mkdir app
cd app || exit

echo "
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'SofIA API tá online, brabo!'}
" > main.py

cd ..

# === Mensagem final ===
echo "✅ Projeto SofIA criado e pronto pra rodar!"
echo "🔁 Ative com: source venv/Scripts/activate"
echo "🚀 Rode com: uvicorn app.main:app --reload"