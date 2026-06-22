import os
from pypdf import PdfReader
import chromadb
from chromadb.utils import embedding_functions
from langchain_core.tools import Tool
from pydantic import BaseModel, Field

# ChromaDB client — local storage mein save hoga
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Default embedding function use karenge (free, local)
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

collection = chroma_client.get_or_create_collection(
    name="documents",
    embedding_function=embedding_fn
)


def load_pdf(file_path: str) -> str:
    """PDF file ko load karke ChromaDB mein store karo"""
    try:
        reader = PdfReader(file_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"

        # Text ko chunks mein todo (har chunk ~500 characters)
        chunk_size = 500
        chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]

        # Purane document ke chunks hatao (agar same naam ka document phir se load ho)
        file_name = os.path.basename(file_path)
        
        # ChromaDB mein store karo
        ids = [f"{file_name}_{i}" for i in range(len(chunks))]
        collection.upsert(
            documents=chunks,
            ids=ids,
            metadatas=[{"source": file_name} for _ in chunks]
        )

        return f"'{file_name}' successfully load ho gaya! {len(chunks)} chunks store hue."

    except Exception as e:
        return f"PDF load karne mein error: {str(e)}"


def query_documents(question: str) -> str:
    """Document Q&A — relevant chunks dhundo"""
    try:
        results = collection.query(
            query_texts=[question],
            n_results=3
        )

        docs = results.get("documents", [[]])[0]

        if not docs:
            return "Koi relevant document nahi mila. Pehle koi PDF load karo."

        context = "\n\n".join(docs)
        return context

    except Exception as e:
        return f"Document search mein error: {str(e)}"


class DocQueryInput(BaseModel):
    question: str = Field(description="The question to search for in uploaded documents")


document_search_tool = Tool(
    name="document_search",
    func=query_documents,
    description="Use this to search information from uploaded PDF documents. Input should be a question or topic to search for.",
    args_schema=DocQueryInput
)