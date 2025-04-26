import os # main.py
import sys
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from rag_chain import build_rag_chain
from rag_chain import ask_sofia
from app.models.prompt_sofia import SOFIA_PROMPT
from app.models.rag_chain_builder import llm

# Inicializa a cadeia uma vez
rag_chain = build_rag_chain(llm, SOFIA_PROMPT)


st.title("Sofia RAG")

user_input = st.text_input("Faça sua pergunta para a Sofia:")
if user_input:
    resposta = ask_sofia(user_input, rag_chain)
    st.write(resposta)
