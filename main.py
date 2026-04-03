from fastapi import FastAPI
from pydantic import BaseModel
from database import add_stock, get_stocks
from ai import ask_about_stocks, ingest_documents

app = FastAPI()


class Stock(BaseModel):
    name: str
    buy_price: float
    amount: int
    sell_price: float
    date: str


@app.get("/")
def home():
    return {"message": "Stock tracker is running"}


@app.get("/stocks")
def get_stocks_api():
    return get_stocks()


@app.post("/stocks")
def add_stock_api(stock: Stock):
    add_stock(stock.name, stock.buy_price, stock.amount, stock.sell_price, stock.date)
    return {"message": "Stock added successfully"}


@app.get("/ask")
def ask_ai(question: str):
    answer = ask_about_stocks(question)
    return {"answer": answer}


@app.post("/ingest")
def ingest_docs():
    """Ingest financial documents from the docs folder into ChromaDB."""
    count = ingest_documents()
    return {"message": f"Ingested {count} new chunks"}
