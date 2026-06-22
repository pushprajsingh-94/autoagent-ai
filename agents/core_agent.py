from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=GROQ_API_KEY,
    temperature=0.3,
)

def create_agent(tools: list):
    """Tools ko LLM se bind karo"""
    llm_with_tools = llm.bind_tools(tools)
    return llm_with_tools