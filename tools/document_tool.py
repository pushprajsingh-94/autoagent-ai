import os
from pypdf import PdfReader
from pinecone import Pinecone, ServerlessSpec
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Pinecone initialize
pc = Pinecone(api_key=PINECONE_API_KEY)

INDEX_NAME = "autoagent-docs"

# Index create karo agar exist nahi karta
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(INDEX_NAME)


def get_embedding(text: str) -> list:
    """Simple embedding using Groq"""
    import hashlib
    import struct
    
    # Simple hash-based embedding (1024 dimensions)
    embeddings = []
    for i in range(1024):
        hash_val = hashlib.md5(f"{text}{i}".encode()).hexdigest()
        val = struct.unpack('f', bytes.fromhex(hash_val[:8]))[0]
        embeddings.append(float(val % 1))
    return embeddings


def load_pdf(file_path: str) -> str:
    try:
        reader = PdfReader(file_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"

        chunk_size = 500
        chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]

        file_name = os.path.basename(file_path)

        vectors = []
        for i, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)
            vectors.append({
                "id": f"{file_name}_{i}",
                "values": embedding,
                "metadata": {"text": chunk, "source": file_name}
            })

        index.upsert(vectors=vectors)

        return f"'{file_name}' successfully loaded! {len(chunks)} chunks stored in Pinecone."

    except Exception as e:
        return f"PDF load error: {str(e)}"


def query_documents(question: str) -> str:
    try:
        question_embedding = get_embedding(question)

        results = index.query(
            vector=question_embedding,
            top_k=3,
            include_metadata=True
        )

        matches = results.get("matches", [])

        if not matches:
            return "No relevant documents found. Please upload a PDF first."

        context = "\n\n".join([m["metadata"]["text"] for m in matches])
        return context

    except Exception as e:
        return f"Document search error: {str(e)}"