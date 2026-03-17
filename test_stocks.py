from database import add_stock, get_stocks

def test_profit_calculation():
    add_stock("Test", 150, 20, 180, "2024-01-15")
    stocks = get_stocks()
    last_stock = stocks[-1]
    assert last_stock["profit"] == 600

def test_total_value_calculation():
    add_stock("Test", 150, 20, 180, "2024-01-15")
    stocks = get_stocks()
    last_stock = stocks[-1]
    assert last_stock["total_value"] == 3000