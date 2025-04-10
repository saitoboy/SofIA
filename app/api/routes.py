from fastapi import APIRouter
from pydantic import BaseModel
from app.models.context_loader import load_context_from_csv
from app.services.sofia_logic import responder_ao_usuario

router = APIRouter()

class Mensagem(BaseModel):
    texto: str

@router.post("/mensagem")
def processar_mensagem(mensagem: Mensagem):
    resposta = responder_ao_usuario(mensagem.texto)
    return {"resposta": resposta}

# Novo endpoint para testar o carregamento de contexto
@router.get("/test-context")
def test_context(file_path: str):
    """
    Endpoint para testar o carregamento de contexto de um arquivo CSV.
    """
    try:
        context = load_context_from_csv(file_path)
        return {"success": True, "context": context}
    except Exception as e:
        return {"success": False, "error": str(e)}
