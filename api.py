from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_groq import ChatGroq
from tools.search_tool import web_search
from tools.document_tool import load_pdf, query_documents
from auth import authenticate_user, create_access_token
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=GROQ_API_KEY,
    temperature=0.3,
)

app = FastAPI(title="AutoAgent API", description="Built by Pushpraj Singh")


class ChatRequest(BaseModel):
    message: str


class PDFRequest(BaseModel):
    file_path: str


class LoginRequest(BaseModel):
    username: str
    password: str


def needs_search(user_input: str) -> bool:
    search_keywords = ["search", "latest", "today", "news", "current", "recent", "now", "price", "weather"]
    if any(keyword in user_input.lower() for keyword in search_keywords):
        return True
    check_prompt = f"""Does answering this question require current/recent internet information? Answer ONLY "YES" or "NO".
Question: {user_input}"""
    response = llm.invoke([{"role": "user", "content": check_prompt}])
    return "YES" in response.content.upper()


@app.get("/")
def home():
    return {"message": "AutoAgent API is running!", "built_by": "Pushpraj Singh"}


@app.post("/login")
def login(request: LoginRequest):
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token({"sub": user["username"]})
    return {
        "access_token": token,
        "username": user["username"],
        "full_name": user["full_name"]
    }


@app.post("/chat")
def chat(request: ChatRequest):
    user_input = request.message

    if user_input.lower().startswith("doc:"):
        question = user_input.split(":", 1)[1].strip()
        context = query_documents(question)
        final_prompt = f"""Answer the question based on this document context.
Context: {context}
Question: {question}
Give a clear answer."""
        response = llm.invoke([{"role": "user", "content": final_prompt}])
        return {"response": response.content}

    if needs_search(user_input):
        search_results = web_search(user_input)
        final_prompt = f"""Based on this search information, answer the question.
Search results: {search_results}
Question: {user_input}
Give a clear, well-organized answer."""
        response = llm.invoke([{"role": "user", "content": final_prompt}])
        return {"response": response.content}

    response = llm.invoke([{"role": "user", "content": user_input}])
    return {"response": response.content}


@app.post("/upload-pdf")
def upload_pdf(request: PDFRequest):
    result = load_pdf(request.file_path)
    return {"result": result}