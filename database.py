import sqlite3

DB_NAME = "stocks.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            buy_price REAL NOT NULL,
            amount INTEGER NOT NULL,
            sell_price REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


create_table()


def add_stock(name: str, buy_price: float, amount: int, sell_price: float, date: str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO stocks (name, buy_price, amount, sell_price, date) VALUES (?, ?, ?, ?, ?)",
        (name, buy_price, amount, sell_price, date)
    )
    conn.commit()
    conn.close()


def get_stocks():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM stocks").fetchall()
    conn.close()
    stocks = []
    for row in rows:
        stock = dict(row)
        stock["profit"] = (stock["sell_price"] - stock["buy_price"]) * stock["amount"]
        stock["total_value"] = stock["sell_price"] * stock["amount"]
        stocks.append(stock)
    return stocks
