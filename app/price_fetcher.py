import yfinance as yf

async def fetch_yahoo(symbol):
    data = yf.Ticker(symbol).history(period="1d")
    if data.empty:
        return None
    return float(data['Close'][-1])
