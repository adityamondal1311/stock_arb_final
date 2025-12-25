import asyncio
import yfinance as yf
from ..config import STOCKS, FETCH_INTERVAL
from ..redis_client import redis

async def fetch_stock(symbol):
    data = yf.download(symbol, period="1d", interval="1m")
    if not data.empty:
        return float(data["Close"].iloc[-1])
    return None

async def price_fetcher():
    while True:
        for nse, bse in STOCKS:
            nse_price = await fetch_stock(nse)
            bse_price = await fetch_stock(bse)

            if nse_price:
                await redis.set(nse, nse_price)
            if bse_price:
                await redis.set(bse, bse_price)

        await asyncio.sleep(FETCH_INTERVAL)

def start_price_fetcher():
    asyncio.get_event_loop().create_task(price_fetcher())
