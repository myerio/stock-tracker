# Stock Tracker API

A REST API that tracks your stock portfolio and automatically calculates profit and total value for each position.

## Features
- Add stocks with buy price, sell price, amount and date
- Automatic profit calculation per stock
- Automatic total value calculation
- Persistent storage with SQLite database
- Unit tested

## AI Assistant
- GET /ask?question=your question - Ask AI about your portfolio
- Powered by Mistral running locally via Ollama
- Example: "Which is my most profitable stock?"

## Technologies Used
- Python
- FastAPI
- SQLite
- Pytest

## How to Run

### Install dependencies
pip install fastapi uvicorn pytest

### Start the server
python -m uvicorn main:app --reload

### Run tests
python -m pytest test_stocks.py -v

### API Endpoints
- GET /stocks - Returns all stocks
- POST /stocks - Adds a new stock

## API Example
POST /stocks
{
  "name": "Apple",
  "buy_price": 150,
  "amount": 20,
  "sell_price": 180,
  "date": "2024-01-15"
}