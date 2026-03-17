import sqlite3

def init_db():
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY,
            name TEXT,
            buy_price REAL,
            amount INTEGER,
            sell_price REAL,
            date TEXT,
            total_value REAL,
            profit REAL
        )
    """)
    conn.commit()
    conn.close()

def add_stock(name, buy_price, amount, sell_price, date):
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO stocks (name, buy_price, amount, sell_price, date, total_value, profit)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, buy_price, amount, sell_price, date, buy_price * amount, (sell_price - buy_price) * amount))
    conn.commit()
    conn.close()


def get_stocks():
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stocks")
    rows = cursor.fetchall()
    conn.close()
    
    stocks = []
    for row in rows:
        stocks.append({
            "id": row[0],
            "name": row[1],
            "buy_price": row[2],
            "amount": row[3],
            "sell_price": row[4],
            "date": row[5],
            "total_value": row[6],
            "profit": row[7]
        })
    return stocks

init_db()