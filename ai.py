import ollama
from database import get_stocks

def ask_about_stocks(question: str):
    stocks = get_stocks()
    
    prompt = f"""You are a stock portfolio assistant.
Here is the user's stock data:
{stocks}

Answer this question: {question}"""
    
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response["message"]["content"]