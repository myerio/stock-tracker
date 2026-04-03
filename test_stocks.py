from database import add_stock, get_stocks
from ai import chunk_text, generate_chunk_id, keyword_search, hybrid_search


# Database tests

def test_profit_calculation():
    add_stock("Test", 150, 20, 180, "2024-01-15")
    stocks = get_stocks()
    last_stock = stocks[-1]
    assert last_stock["profit"] == 600


def test_total_value_calculation():
    add_stock("Test", 150, 20, 180, "2024-01-15")
    stocks = get_stocks()
    last_stock = stocks[-1]
    assert last_stock["total_value"] == 3600


def test_add_multiple_stocks():
    add_stock("Apple", 150, 10, 180, "2024-01-15")
    add_stock("Microsoft", 300, 5, 350, "2024-02-10")
    stocks = get_stocks()
    names = [s["name"] for s in stocks]
    assert "Apple" in names
    assert "Microsoft" in names


def test_negative_profit():
    add_stock("Loser", 200, 10, 150, "2024-03-01")
    stocks = get_stocks()
    last_stock = stocks[-1]
    assert last_stock["profit"] == -500


# RAG component tests

def test_chunk_text_basic():
    text = "A" * 1000
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    assert len(chunks) >= 2
    assert len(chunks[0]) == 500


def test_chunk_text_small():
    text = "Short text"
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    assert len(chunks) == 1
    assert chunks[0] == "Short text"


def test_chunk_text_overlap():
    text = "ABCDEFGHIJ" * 100  # 1000 chars
    chunks = chunk_text(text, chunk_size=500, overlap=100)
    # With overlap, end of chunk 1 should appear at start of chunk 2
    end_of_first = chunks[0][-100:]
    start_of_second = chunks[1][:100]
    assert end_of_first == start_of_second


def test_chunk_text_empty():
    chunks = chunk_text("")
    assert len(chunks) == 0


def test_generate_chunk_id_unique():
    id1 = generate_chunk_id("file1.txt", 0)
    id2 = generate_chunk_id("file1.txt", 1)
    id3 = generate_chunk_id("file2.txt", 0)
    assert id1 != id2
    assert id1 != id3
    assert id2 != id3


def test_generate_chunk_id_deterministic():
    id1 = generate_chunk_id("file1.txt", 0)
    id2 = generate_chunk_id("file1.txt", 0)
    assert id1 == id2
