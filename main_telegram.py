import os
from dotenv import load_dotenv

from app.rag_chain.rag_chain import build_rag_chain
from app.models.rag_chain_builder import llm
from app.models.prompt_sofia import SOFIA_PROMPT
from app.utils.bot_telegram import run_telegram_bot

load_dotenv()

TELEGRAM_API = os.getenv("TELEGRAM_API")

if __name__ == "__main__":
    print("🚀 Iniciando SofiA com Telegram + RAG + LLM...")
    rag_chain = build_rag_chain(llm, SOFIA_PROMPT)
    run_telegram_bot(TELEGRAM_API, rag_chain)
