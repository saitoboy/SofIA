import sys
import os
import html  # Importa para escapar caracteres especiais no HTML
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import streamlit as st
from app.models.langchain_integration import ask_gemini
from app.models.context_loader import load_context_from_csv, load_context_from_pdf, load_default_pdf_context

# Configuração inicial do Streamlit
st.set_page_config(page_title="Sofia - Assistente Virtual", layout="wide")

# Inicializa o histórico de mensagens na sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# SIDEBAR - menu lateral
with st.sidebar:
    st.image(
        "https://guilhermesaito.com.br/wp-content/uploads/2025/04/sofia_Prancheta-1-copia-4.png",
        use_container_width=True
    )
    st.title("A assistente perfeita para cada time!")
    st.markdown("### Configurações")
    
    # Carrega automaticamente o PDF institucional
    pdf_context = None
    csv_context = None
    try:
        pdf_context = load_default_pdf_context()
        st.sidebar.success("Contexto do PDF institucional carregado com sucesso!")
    except FileNotFoundError as e:
        st.sidebar.warning(f"Arquivo PDF não encontrado: {e}")
    except Exception as e:
        st.sidebar.error(f"Erro ao carregar o contexto do PDF: {e}")
    
    # Carrega automaticamente os dados do CSV
    try:
        csv_context = load_context_from_csv("d:\\SofIA\\app\\data\\dados.csv")  # Substitua pelo caminho correto do CSV
        st.sidebar.success("Contexto dos dados CSV carregado com sucesso!")
    except FileNotFoundError as e:
        st.sidebar.warning(f"Arquivo CSV não encontrado: {e}")
    except Exception as e:
        st.sidebar.error(f"Erro ao carregar o contexto do CSV: {e}")

    # Combina os contextos (se ambos forem carregados)
    if pdf_context and csv_context:
        combined_context = f"{pdf_context}\n\n{csv_context}"
    elif pdf_context:
        combined_context = pdf_context
    elif csv_context:
        combined_context = csv_context
    else:
        combined_context = None

# TÍTULO PRINCIPAL
st.title("💬 Sofia - Assistente Virtual")
st.write("Digite algo para começar:")

# Função para renderizar mensagens com estilo de bolha
def render_message(message, role):
    # Escapa caracteres especiais no conteúdo da mensagem
    escaped_message = html.escape(message)
    if role == "user":
        color = "#DCF8C6"  # verde claro (usuário)
        align = "right"
    else:
        color = "#F1F0F0"  # cinza claro (assistente)
        align = "left"

    html_code = f"""
    <div style='background-color: {color}; padding: 10px; border-radius: 10px;
                margin: 5px 0; text-align: {align}; max-width: 75%;
                float: {align}; clear: both;'>
        {escaped_message}
    """
    st.markdown(html_code, unsafe_allow_html=True)

# Renderiza as mensagens anteriores
for msg in st.session_state.messages:
    render_message(msg["content"], msg["role"])

# Entrada do usuário (campo de texto)
if combined_context:
    prompt = st.chat_input("Escreva sua mensagem...")

    if prompt:
        # Armazena e renderiza a mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        render_message(prompt, "user")

        # Geração/resposta do assistente usando a API Gemini
        with st.spinner("Sofia está pensando..."):
            try:
                response = ask_gemini(combined_context, prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
                render_message(response, "assistant")
            except Exception as e:
                st.error(f"Erro ao processar a pergunta: {e}")
else:
    st.error("Nenhum contexto foi carregado. Verifique os arquivos PDF e CSV.")
