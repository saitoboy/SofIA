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

# Função de alerta customizado com borda escura e suporte a HTML opcional
def custom_alert(message, alert_type="info", allow_html=False):
    colors = {
        "info": "#3498db",
        "success": "#2ecc71",
        "warning": "#f39c12",
        "error": "#e74c3c"
    }
    bg_color = colors.get(alert_type, "#3498db")

    content = html.escape(message) if not allow_html else message

    html_code = f"""
    <div style='
        background-color: {bg_color};
        color: white;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid black;
        margin-bottom: 10px;
        font-family: sans-serif;
    '>{content}</div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

# SIDEBAR - menu lateral
with st.sidebar:
    st.image(
        "https://guilhermesaito.com.br/wp-content/uploads/2025/04/sofia_Prancheta-1-copia-4.png",
        use_container_width=True
    )
    st.title("A assistente perfeita para cada time!")
    st.markdown("### Configurações")

    # Tema com estilo toggle
    selected = st.toggle("🌙 Modo Escuro", value=False, help="Ative para modo escuro")
    theme = "Escuro" if selected else "Claro"
    st.session_state["theme"] = theme

    # Carrega o PDF institucional
    pdf_context = None
    try:
        pdf_context = load_default_pdf_context()
        custom_alert("Contexto do PDF institucional carregado com sucesso!", "success")
    except FileNotFoundError as e:
        custom_alert(f"Arquivo PDF não encontrado: {e}", "warning")
    except Exception as e:
        custom_alert(f"Erro ao carregar o contexto do PDF: {e}", "error")

    # Carrega todos os arquivos CSV da pasta 'data'
    csv_context = ""
    try:
        csv_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        csv_files = glob.glob(os.path.join(csv_folder_path, "*.csv"))
        if csv_files:
            nomes_formatados = "; ".join([os.path.splitext(os.path.basename(f))[0] for f in csv_files])
            mensagem_csv = f"Arquivos CSV encontrados: {len(csv_files)}<br> Nomes: {nomes_formatados}"
            custom_alert(mensagem_csv, "info", allow_html=True)
            for csv_file in csv_files:
                try:
                    content = load_context_from_csv(csv_file, for_langchain=True)
                    csv_context += f"\n\n{content}"
                except Exception as e:
                    custom_alert(f"Erro ao carregar {os.path.basename(csv_file)}: {e}", "warning")
            custom_alert("Todos os arquivos CSV foram carregados com sucesso!", "success")
        else:
            custom_alert("Nenhum arquivo CSV encontrado na pasta 'data'.", "warning")
    except Exception as e:
        custom_alert(f"Erro ao carregar os arquivos CSV: {e}", "error")

    # Combina os contextos (se ambos forem carregados)
    if pdf_context and csv_context:
        combined_context = f"{pdf_context}\n\n{csv_context}"
    elif pdf_context:
        combined_context = pdf_context
    elif csv_context:
        combined_context = csv_context
    else:
        combined_context = None

    # Limite de tokens por minuto - evita erro 413 na API
    MAX_CONTEXT_CHARS = 5000
    if combined_context and len(combined_context) > MAX_CONTEXT_CHARS:
        combined_context = combined_context[:MAX_CONTEXT_CHARS]
        custom_alert("\u26a0\ufe0f O contexto foi truncado para evitar ultrapassar o limite da API.", "warning")

# TÍTULO PRINCIPAL
st.title("💬 Sofia - Assistente Virtual")
st.write("Digite algo para começar:")

# Função para renderizar mensagens com estilo WhatsApp
def render_message(message, role):
    escaped_message = html.escape(message)
    theme = st.session_state.get("theme", "Claro")

    if theme == "Claro":
        user_bg = "#25D366"
        ai_bg = "#ECECEC"
        text_color = "black"
    else:
        user_bg = "#005c4b"
        ai_bg = "#202c33"
        text_color = "white"

    background_color = user_bg if role == "user" else ai_bg
    align = "right" if role == "user" else "left"

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
