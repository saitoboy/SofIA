import sys
import os
import html
import glob
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from app.models.langchain_integration import ask_groq
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

    # Carrega o PDF institucional
    pdf_context = None
    csv_context = ""
    try:
        pdf_context = load_default_pdf_context()
        st.sidebar.success("Contexto do PDF institucional carregado com sucesso!")
    except FileNotFoundError as e:
        st.sidebar.warning(f"Arquivo PDF não encontrado: {e}")
    except Exception as e:
        st.sidebar.error(f"Erro ao carregar o contexto do PDF: {e}")

    # Carrega todos os arquivos CSV da pasta 'data'
    try:
        csv_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        csv_files = glob.glob(os.path.join(csv_folder_path, "*.csv"))
        st.sidebar.info(f"Arquivos CSV encontrados: {csv_files}")

        if csv_files:
            for csv_file in csv_files:
                try:
                    content = load_context_from_csv(csv_file, for_langchain=True)
                    csv_context += f"\n\n{content}"
                except Exception as e:
                    st.sidebar.warning(f"Erro ao carregar {csv_file}: {e}")
            st.sidebar.success("Todos os arquivos CSV foram carregados com sucesso!")
        else:
            st.sidebar.warning("Nenhum arquivo CSV encontrado na pasta 'data'.")
    except Exception as e:
        st.sidebar.error(f"Erro ao carregar os arquivos CSV: {e}")

    # Combina os contextos (se ambos forem carregados)
    if pdf_context and csv_context:
        combined_context = f"{pdf_context}\n\n{csv_context}"
    elif pdf_context:
        combined_context = pdf_context
    elif csv_context:
        combined_context = csv_context
    else:
        combined_context = None

# Limite aproximado para evitar exceder o TPM do Groq (6000 tokens ≈ 5000-6000 caracteres)
MAX_CONTEXT_CHARS = 5000

# Trunca o contexto se necessário
if combined_context and len(combined_context) > MAX_CONTEXT_CHARS:
    combined_context = combined_context[:MAX_CONTEXT_CHARS]
    st.sidebar.warning("⚠️ O contexto foi truncado para evitar ultrapassar o limite da API.")

# TÍTULO PRINCIPAL
st.title("💬 Sofia - Assistente Virtual")
st.write("Digite algo para começar:")

# (importações e carregamento de contexto mantidos como antes...)

# Função para renderizar mensagens com estilo WhatsApp
def render_message(message, role):
    escaped_message = html.escape(message)

    if role == "user":
        background_color = "#005c4b"  # Verde WhatsApp (usuário)
        text_color = "white"
        align = "right"
    else:
        background_color = "#202c33"  # Cinza escuro para contraste com texto branco
        text_color = "white"
        align = "left"

    html_code = f"""
    <div style='
        background-color: {background_color};
        color: {text_color};
        padding: 10px;
        border-radius: 10px;
        border: 1px solid black;
        margin: 5px 0;
        text-align: {align};
        max-width: 75%;
        float: {align};
        clear: both;
    '>
        {escaped_message}
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)



# Renderiza mensagens anteriores
for msg in st.session_state.messages:
    render_message(msg["content"], msg["role"])

# Entrada do usuário
if combined_context:
    prompt = st.chat_input("Escreva sua mensagem...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        render_message(prompt, "user")

        with st.spinner("Sofia está pensando..."):
            try:
                response = ask_groq(combined_context, prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
                render_message(response, "assistant")
            except Exception as e:
                st.error(f"Erro ao processar a pergunta: {e}")
else:
    st.error("Nenhum contexto foi carregado. Verifique os arquivos PDF e CSV.")
