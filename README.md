# 🤖 SofiA - Assistente Virtual com RAG + Telegram

SofiA é uma assistente virtual desenvolvida para suporte interno de equipes comerciais e operacionais, utilizando **RAG (Retrieval-Augmented Generation)** com integração a **GroqAI** (compatível também com **OpenAI**). Ela é capaz de ler documentos `.csv` e `.pdf`, realizar buscas inteligentes em base de dados (Pinecone) e atender tanto via **interface Streamlit** quanto via **Telegram Bot**.

---

## 🚀 Funcionalidades principais

- ✅ Leitura de múltiplos `.csv`, `.pdf` e arquivos do Google Drive
- ✅ Integração RAG moderna (`create_retrieval_chain`) com LangChain
- ✅ Busca semântica otimizada por embeddings da Cohere
- ✅ Persistência de contexto inteligente em Pinecone
- ✅ Interface no **Streamlit** estilo WhatsApp, com tema claro/escuro
- ✅ Integração via **Telegram Bot** oficial
- ✅ Controle automático de limites de tokens (respeitando planos gratuitos)

---

## ⚙️ Como executar o projeto

Clone o repositório e instale as dependências:

```bash
pip install -r requirements.txt
```

### 1. Rodar SofiA no navegador (modo Streamlit, pasta local)

```bash
python run_integration.py
```

### 2. Rodar SofiA no terminal (teste rápido)

```bash
python app/rag_chain/rag_chain.py
```

### 3. Rodar SofiA no Telegram Bot

Configure seu token no `.env` e execute:

```bash
python main_telegram.py
```

---

## 🔐 Configurações de API necessárias

- **Groq API Key** (GROQ_API_KEY)
- **Cohere API Key** (COHERE_API_KEY)
- **Pinecone API Key + Host** (PINECONE_API_KEY, PINECONE_INDEX)
- **Telegram Bot Token** (TELEGRAM_API)

Todas as variáveis devem estar no seu `.env` na raiz do projeto.

---

## 💡 Tecnologias utilizadas

- **Python 3.11+**
- **Streamlit**
- **Telegram Bot (python-telegram-bot)**
- **LangChain (v0.1+ - LCEL)**
- **Groq / OpenAI**
- **Cohere Embeddings**
- **Pinecone Vector Database**
- **Google Drive API**
- **Pandas**, **PyPDF2**, **Glob**, **dotenv**

---

## 🛠️ Funcionalidades futuras

- Melhorias visuais no Streamlit (componentes nativos para upload)
- Integração com WhatsApp via API (Cloud API / Z-API)
- Armazenamento de histórico de conversa em banco de dados
- Logs de conversação para análises internas
- Sistema de usuários autenticados para gestão de permissões

---

## 📄 Pull Requests

Este projeto possui um [template padrão de Pull Request](.github/pull_request_template.md) para facilitar revisões e padronizar entregas.

---

## 👨‍💻 Como contribuir

- Faça um fork do projeto
- Crie uma branch com sua feature (`git checkout -b feature/sua-feature`)
- Commit suas alterações (`git commit -m 'feat: Minha nova feature'`)
- Faça o push para o seu fork (`git push origin feature/sua-feature`)
- Abra um Pull Request

---

## 📌 Observações

- A SofiA é destinada **exclusivamente para uso interno** no Grupo Houer.
- Sua comunicação é empática, positiva e alinhada aos valores da empresa.
- Não substitui o atendimento humano em situações críticas ou sensíveis.

---

## 🧠 Exemplo de fluxo de uso

```text
Usuário: Quais são os municípios que temos acesso em Rondônia?
Sofia: De acordo com os dados disponíveis, temos acesso aos municípios: Cerejeiras, Colorado do Oeste, Corumbiara, Costa Marques...

Usuário: Qual a CAPAG do município de Niterói (RJ)?
Sofia: Para Niterói (RJ), a classificação CAPAG é A, com base nos indicadores analisados em 2023.
```

---

> Projeto interno para otimização de atendimento e apoio comercial 🌟