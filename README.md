# 🤖 AutoAgent AI

> An intelligent AI agent with real-time web search, document Q&A, and RAG capabilities.

**Built by Pushpraj Singh**

---

## 🚀 Live Demo
*Coming soon — deployment in progress*

---

## ✨ Features

- 🌐 **Real-time Web Search** — Searches the internet using Tavily API
- 📄 **Document Q&A (RAG)** — Upload any PDF and ask questions about it
- 🧠 **General Knowledge** — Powered by Groq LLaMA 3.1
- 🔐 **Authentication** — JWT-based login system
- ⚡ **Fast API Backend** — Built with FastAPI
- 🎨 **Professional UI** — Built with Streamlit

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Groq LLaMA 3.1 8B |
| Web Search | Tavily API |
| Vector DB | ChromaDB |
| Backend | FastAPI |
| Frontend | Streamlit |
| Auth | JWT (python-jose) |
| Language | Python 3.11 |

---

## ⚙️ Setup

1. Clone: git clone https://github.com/pushprajsingh-94/autoagent-ai.git
2. Install: pip install -r requirements.txt
3. Add .env file with GROQ_API_KEY and TAVILY_API_KEY
4. Run API: uvicorn api:app --reload
5. Run UI: streamlit run app.py
6. Open: http://localhost:8501
7. Login: demo / demo123

---

## 📁 Project Structure

agents/core_agent.py — LLM agent logic
tools/search_tool.py — Tavily web search
tools/document_tool.py — PDF Q&A with RAG
api.py — FastAPI backend
app.py — Streamlit frontend
auth.py — JWT authentication

---

## How It Works

User → Streamlit UI → FastAPI → AI Agent → Web Search / Doc Q&A / Direct Answer → Response

---

## 👤 Author

**Pushpraj Singh**
B.Tech CSE (AI & ML)
GitHub: https://github.com/pushprajsingh-94

---

Built with heart by Pushpraj Singh