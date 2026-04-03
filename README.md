# Stock Tracker API

A REST API that tracks your stock portfolio and uses a RAG (Retrieval Augmented Generation) pipeline to answer questions about your stocks using financial documents as context.

## Features

- Add stocks with buy price, sell price, amount and date
- Automatic profit and total value calculation per stock
- RAG pipeline with hybrid retrieval (vector + keyword search)
- Financial document ingestion with chunking and embeddings
- Persistent vector storage with ChromaDB
- Persistent portfolio storage with SQLite
- Unit tested with pytest
- Dockerized for deployment
- CI/CD with GitHub Actions

## Architecture

```
User question
    |
    v
Hybrid Search (vector + keyword)
    |
    v
ChromaDB returns relevant document chunks
    |
    v
Chunks + portfolio data sent to Mistral via Ollama
    |
    v
Mistral generates contextual answer
```

### RAG Pipeline

1. **Ingestion**: Financial documents (`.txt`) are read from the `docs/` folder
2. **Chunking**: Documents are split into overlapping chunks (500 chars, 50 char overlap)
3. **Embedding**: Each chunk is embedded using `nomic-embed-text` via Ollama
4. **Storage**: Embeddings are stored in ChromaDB with metadata
5. **Retrieval**: Hybrid search combines vector similarity and keyword matching
6. **Generation**: Mistral generates answers using retrieved context + portfolio data

## Technologies Used

- Python
- FastAPI
- SQLite
- ChromaDB
- Ollama (Mistral + nomic-embed-text)
- Pytest
- Docker
- GitHub Actions CI/CD

## How to Run

### Prerequisites

- Python 3.12+
- Ollama installed with models pulled:

```bash
ollama pull mistral
ollama pull nomic-embed-text
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the server

```bash
python -m uvicorn main:app --reload
```

### Ingest financial documents

Place `.txt` files in the `docs/` folder, then:

```bash
curl -X POST http://localhost:8000/ingest
```

### Run tests

```bash
python -m pytest test_stocks.py -v
```

### Run with Docker

```bash
docker build -t stock-tracker .
docker run -p 8000:8000 stock-tracker
```

Note: When running in Docker, Ollama must be accessible from the container. Set the `OLLAMA_HOST` environment variable if needed.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/stocks` | Returns all stocks |
| POST | `/stocks` | Adds a new stock |
| GET | `/ask?question=...` | Ask AI about your portfolio and financial documents |
| POST | `/ingest` | Ingest documents from the docs folder into ChromaDB |

## API Example

```bash
# Add a stock
curl -X POST http://localhost:8000/stocks \
  -H "Content-Type: application/json" \
  -d '{"name": "Apple", "buy_price": 150, "amount": 20, "sell_price": 180, "date": "2024-01-15"}'

# Ingest financial documents
curl -X POST http://localhost:8000/ingest

# Ask a question using RAG
curl "http://localhost:8000/ask?question=What%20is%20the%20analyst%20recommendation%20for%20Apple"
```
