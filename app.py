import streamlit as st
import requests

API_URL = "https://autoagent-ai-api.onrender.com"

st.set_page_config(
    page_title="AutoAgent AI",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
    }
    .login-container {
        max-width: 400px;
        margin: auto;
        padding: 2rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .footer {
        text-align: center;
        color: #888;
        font-size: 13px;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 1px solid #eee;
    }
    .status-online {
        color: #28a745;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


def login_page():
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AutoAgent AI</h1>
        <p>Intelligent Assistant — Web Search + Document Q&A + Real-time Answers</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Login to Continue")
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")

        if st.button("Login", use_container_width=True):
            if username and password:
                with st.spinner("Authenticating..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/login",
                            json={"username": username, "password": password}
                        )
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.token = data["access_token"]
                            st.session_state.username = data["username"]
                            st.session_state.full_name = data["full_name"]
                            st.session_state.logged_in = True
                            st.rerun()
                        else:
                            st.error("❌ Invalid username or password!")
                    except Exception as e:
                        st.error(f"❌ Cannot connect to API: {str(e)}")
            else:
                st.warning("⚠️ Please enter username and password!")

        st.markdown("---")
        st.markdown("**Demo credentials:**")
        st.code("Username: demo\nPassword: demo123")

    st.markdown("""
    <div class="footer">
        Built by <strong>Pushpraj Singh</strong> | AutoAgent AI v1.0
    </div>
    """, unsafe_allow_html=True)


def main_app():
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.full_name}")
        st.markdown('<p class="status-online">● API Online</p>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("## 📄 Document Upload")
        pdf_path = st.text_input("Enter PDF file path:", placeholder="C:\\Users\\...\\document.pdf")

        if st.button("📤 Load Document", use_container_width=True):
            if pdf_path:
                with st.spinner("Processing document..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/upload-pdf",
                            json={"file_path": pdf_path},
                            headers={"Authorization": f"Bearer {st.session_state.token}"}
                        )
                        result = response.json().get("result", "Error")
                        st.success(f"✅ {result}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please enter a PDF path first.")

        st.markdown("---")
        st.markdown("## 💡 How to Use")
        st.markdown("""
**Direct Question:**
> What is machine learning?

**Web Search:**
> search latest AI news today

**Document Q&A:**
> doc: what are the key skills?
        """)

        st.markdown("---")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        st.markdown("---")
        st.markdown("**Built with:**")
        st.markdown("🔸 Groq LLaMA 3.1 | 🔸 Tavily Search")
        st.markdown("🔸 ChromaDB RAG | 🔸 FastAPI")

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AutoAgent AI</h1>
        <p>Intelligent Assistant — Web Search + Document Q&A + Real-time Answers</p>
    </div>
    """, unsafe_allow_html=True)

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if not st.session_state.messages:
        st.markdown("""
### 👋 Welcome to AutoAgent!

I can help you with:
- 🌐 **Real-time web search** — Get latest information from the internet
- 📄 **Document Q&A** — Upload a PDF and ask questions about it
- 🧠 **General knowledge** — Answer any question from my training

*Type your question below to get started!*
        """)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        f"{API_URL}/chat",
                        json={"message": prompt},
                        headers={"Authorization": f"Bearer {st.session_state.token}"}
                    )
                    answer = response.json().get("response", "Something went wrong.")
                except Exception as e:
                    answer = f"❌ Could not connect to API: {str(e)}"

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

    st.markdown("""
    <div class="footer">
        Built by <strong>Pushpraj Singh</strong> | AutoAgent AI v1.0
    </div>
    """, unsafe_allow_html=True)


# Main logic
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    main_app()
else:
    login_page()