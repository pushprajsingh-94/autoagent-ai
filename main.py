from langchain_groq import ChatGroq
from tools.search_tool import web_search
from tools.document_tool import load_pdf, query_documents
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=GROQ_API_KEY,
    temperature=0.3,
)

def needs_search(user_input: str) -> bool:
    search_keywords = ["search", "latest", "today", "news", "current", "recent", "now", "price", "weather"]
    if any(keyword in user_input.lower() for keyword in search_keywords):
        return True
    check_prompt = f"""Does answering this question require current/recent internet information (like news, prices, latest events)? Answer ONLY "YES" or "NO".

Question: {user_input}"""
    response = llm.invoke([{"role": "user", "content": check_prompt}])
    return "YES" in response.content.upper()


def run_agent(user_input: str):
    print(f"\n{'='*50}")
    print(f"You: {user_input}")
    print(f"{'='*50}\n")

    # Command: PDF load karna
    if user_input.lower().startswith("load pdf:"):
        file_path = user_input.split(":", 1)[1].strip()
        result = load_pdf(file_path)
        print(f"\n{'='*50}")
        print(f"AutoAgent: {result}")
        print(f"{'='*50}\n")
        return result

    # Command: Document se sawal
    if user_input.lower().startswith("doc:"):
        question = user_input.split(":", 1)[1].strip()
        context = query_documents(question)

        final_prompt = f"""Answer the question based on this document context.

Context:
{context}

Question: {question}

Give a clear answer based on the context above."""

        response = llm.invoke([{"role": "user", "content": final_prompt}])
        output = response.content
        print(f"\n{'='*50}")
        print(f"AutoAgent: {output}")
        print(f"{'='*50}\n")
        return output

    # Normal web search ya direct answer
    if needs_search(user_input):
        print(f"🔧 Searching the web for: {user_input}")
        search_results = web_search(user_input)

        final_prompt = f"""Based on this search information, answer the user's question.

Search results:
{search_results}

User question: {user_input}

Give a clear, well-organized answer."""

        response = llm.invoke([{"role": "user", "content": final_prompt}])
        output = response.content
    else:
        response = llm.invoke([{"role": "user", "content": user_input}])
        output = response.content

    print(f"\n{'='*50}")
    print(f"AutoAgent: {output}")
    print(f"{'='*50}\n")

    return output


if __name__ == "__main__":
    print("🤖 AutoAgent Ready!")
    print("Commands:")
    print("  - 'load pdf: path/to/file.pdf' → PDF load karo")
    print("  - 'doc: your question' → document se sawal poocho")
    print("  - 'quit' → band karo\n")

    while True:
        user_input = input("Aap: ").strip()

        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("AutoAgent band ho raha hai...")
            break

        run_agent(user_input)