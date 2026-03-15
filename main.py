from fastapi import FastAPI
from pydantic import BaseModel
from stocks import stocks, add_stock

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
def get_stocks():
    return stocks

@app.post("/stocks")
def add_stock_api(stock: Stock):
    add_stock(stock.name, stock.buy_price, stock.amount, stock.sell_price, stock.date)
    return {"message": "Stock added successfully"}