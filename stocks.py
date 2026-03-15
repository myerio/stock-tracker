import json
try:
    with open("stocks.json", "r") as f:
        stocks = json.load(f)
except:
    stocks = []

def add_stock(name, buy_price, amount, sell_price, date):
    stock = {

        "name": name,
        "buy_price": buy_price,
        "amount": amount,
        "total_value": buy_price * amount,
        "sell_price": sell_price,
        "date": date,
        "profit": (sell_price - buy_price) * amount
    }
    stocks.append(stock)

    with open("stocks.json", "w") as f:
         json.dump(stocks, f)

# add_stock("Apple", 150, 20, 180, "2024-01-15")
# add_stock("Tesla", 200, 5, 250, "2024-02-20")

total_portfolio = 0
for stock in stocks:
    total_portfolio += stock["total_value"]

print(stocks)
print("Total portfolio value:", total_portfolio)