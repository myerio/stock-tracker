import ollama
import chromadb
import os
import hashlib
from pathlib import Path
from database import get_stocks


# Initialize ChromaDB client with persistent storage
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(
    name="financial_docs",
    metadata={"hnsw:space": "cosine"}
)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks for better retrieval."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start += chunk_size - overlap
    return chunks


def generate_chunk_id(filename: str, index: int) -> str:
    """Create a unique ID for each chunk based on filename and position."""
    raw = f"{filename}_{index}"
    return hashlib.md5(raw.encode()).hexdigest()


def embed_text(text: str) -> list[float]:
    """Convert text to a vector using nomic-embed-text via Ollama."""
    response = ollama.embed(model="nomic-embed-text", input=text)
    return response["embeddings"][0]


def ingest_documents(docs_folder: str = "./docs"):
    """Read all .txt files from docs folder, chunk them, embed, and store in ChromaDB."""
    docs_path = Path(docs_folder)
    if not docs_path.exists():
        print(f"No docs folder found at {docs_folder}")
        return 0

    files = list(docs_path.glob("*.txt"))
    if not files:
        print("No .txt files found in docs folder")
        return 0

    total_chunks = 0

    for file_path in files:
        text = file_path.read_text(encoding="utf-8")
        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            chunk_id = generate_chunk_id(file_path.name, i)

            # Skip if already ingested
            existing = collection.get(ids=[chunk_id])
            if existing["ids"]:
                continue

            embedding = embed_text(chunk)

            collection.add(
                ids=[chunk_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"source": file_path.name, "chunk_index": i}]
            )
            total_chunks += 1

    print(f"Ingested {total_chunks} new chunks from {len(files)} files")
    return total_chunks


def vector_search(query: str, n_results: int = 3) -> list[dict]:
    """Find the most relevant chunks using vector similarity search."""
    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    matches = []
    for i in range(len(results["ids"][0])):
        matches.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })
    return matches


def keyword_search(query: str, n_results: int = 3) -> list[dict]:
    """Simple keyword-based search through ChromaDB documents."""
    results = collection.get(
        include=["documents", "metadatas"]
    )

    if not results["documents"]:
        return []

    # Score each document by keyword overlap
    query_words = set(query.lower().split())
    scored = []
    for i, doc in enumerate(results["documents"]):
        doc_words = set(doc.lower().split())
        overlap = len(query_words & doc_words)
        if overlap > 0:
            scored.append({
                "text": doc,
                "source": results["metadatas"][i]["source"],
                "keyword_score": overlap
            })

    scored.sort(key=lambda x: x["keyword_score"], reverse=True)
    return scored[:n_results]


def hybrid_search(query: str, n_results: int = 3) -> list[dict]:
    """Combine vector search and keyword search for better retrieval."""
    vector_results = vector_search(query, n_results=n_results)
    keyword_results = keyword_search(query, n_results=n_results)

    # Merge results, preferring vector matches but adding keyword-only finds
    seen_texts = set()
    merged = []

    for result in vector_results:
        seen_texts.add(result["text"][:100])
        result["method"] = "vector"
        merged.append(result)

    for result in keyword_results:
        if result["text"][:100] not in seen_texts:
            result["method"] = "keyword"
            merged.append(result)

    return merged[:n_results * 2]


def ask_about_stocks(question: str) -> str:
    """Answer questions using hybrid RAG retrieval + portfolio data."""

    # Get portfolio data from SQLite
    stocks = get_stocks()

    # Get relevant document context via hybrid search
    doc_context = ""
    sources = []
    if collection.count() > 0:
        results = hybrid_search(question, n_results=3)
        if results:
            doc_chunks = [r["text"] for r in results]
            sources = list(set(r["source"] for r in results))
            doc_context = "\n\n".join(doc_chunks)

    prompt = f"""You are a stock portfolio assistant with access to financial documents and portfolio data.

Portfolio data:
{stocks}

Relevant financial context:
{doc_context if doc_context else "No relevant documents found."}

Answer this question: {question}

If you use information from the financial documents, mention which source you are referencing."""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response["message"]["content"]

    if sources:
        answer += f"\n\nSources: {', '.join(sources)}"

    return answer
