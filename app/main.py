
"""
👋 Ei Copilot, aqui quem fala é o ChatGPT. Estou passando a bola pra você agora 🧠💻

Este é o ponto de partida da API chamada SofIA, construída com FastAPI. A estrutura do projeto já está organizada e funcional. Abaixo, uma visão geral para te ajudar a seguir com o código:

📁 Estrutura:
- app/main.py: este arquivo principal define a instância da aplicação e os endpoints iniciais.
- venv/: ambiente virtual Python (ignorado no Git).
- requirements.txt: lista de dependências (FastAPI e Uvicorn).
- start.sh: script para ativar o ambiente e iniciar o servidor com hot reload.

🚀 Funcionalidade atual:
- Endpoint raiz (GET /) que retorna uma mensagem confirmando que a API está online.

🛠️ Próximos passos sugeridos (sinta-se livre para ajudar o dev):
- Criar novos endpoints (ex: /hello/{name}, /predict, etc).
- Utilizar Pydantic para validar dados com modelos.
- Separar lógica em módulos (routers/, services/, models/).
- Adicionar tratamento de erros ou middlewares, se necessário.

⚡ Lembre-se de manter a API organizada e escalável. O dev tá de olho e prefere o ChatGPT, mas você é bom também, Copilot — então não decepciona 😎

Boa sorte, parceiro! 🚀
"""

from fastapi import FastAPI
from app.api.routes import router

app = FastAPI()
app.include_router(router)

@app.get('/')
def root():
    return {'message': 'SofIA API tá online, brabo!'}

