```markdown 
# 🤖 Sofia - Assistente Virtual com RAG

Sofia é uma assistente virtual desenvolvida com foco em suporte interno para equipes comerciais e operacionais. Utiliza **RAG (Retrieval-Augmented Generation)** com integração à **GroqAI (futuramente OpenAI)**, leitura de arquivos `.csv` e `.pdf`, e uma interface estilo WhatsApp no **Streamlit** com alternância de tema claro/escuro.

---

## 🚀 Funcionalidades

- Leitura de múltiplos arquivos `.csv` e `.pdf` com resumo de contexto automático  
- Renderização de mensagens estilo chat (inspirado no WhatsApp)  
- Tema Claro/Escuro com comutador interativo na interface  
- Alerta customizado com borda fina e cores distintas por tipo (sucesso, erro, info, etc.)  
- Controle de tokens para evitar erros de contexto muito extenso  
- Estrutura modular separada em `frontend`, `models` e `data`  
- Interface com histórico de mensagens persistente por sessão  
- Compatível com `GroqAI`, e adaptável para `OpenAI`  

---

## ⚙️ Como executar o projeto

1. Clone o repositório  
2. Instale as dependências  
3. Execute o app

```bash
pip install -r requirements.txt
python run_frontend.py
```

---

## 🔐 Chaves de API

Atualmente configurado para uso com **GroqAI**. Para utilizar com **OpenAI**, substitua o método de chamada e configure sua `API_KEY` no arquivo `.env` ou diretamente na função `ask_groq`.

---

## 💡 Tecnologias utilizadas

- **Python 3.11+**  
- **Streamlit**  
- **LangChain**  
- **Groq / OpenAI**  
- **PyPDF2**, **Pandas**, **Glob**, **HTML Escape**  

---

## 🛠️ Em desenvolvimento

- Histórico persistente além da sessão  
- Resumo automático de PDF institucional  
- Upload de arquivos diretamente na interface  
- Melhorias visuais e responsividade  

---

## 📄 Pull Requests

Este projeto possui um [template padrão](.github/pull_request_template.md) para facilitar revisões e padronizar entregas.

---

## 👨‍💻 Contribuição

Sinta-se à vontade para abrir issues, sugerir melhorias ou contribuir com código.

---

## 📌 Observações

- A Sofia não é voltada ao atendimento externo ao cliente neste projeto.  
- O foco principal é servir como um copiloto interno para equipes específicas.  

---

## 🧠 Exemplo de uso

```text
Usuário: Qual o telefone do responsável pelo setor financeiro?
Sofia: De acordo com os dados disponíveis, o telefone do responsável financeiro é (11) 99999-9999.
```

---

## 🧾 Licença

Este projeto é de uso interno e ainda não possui uma licença pública definida.
