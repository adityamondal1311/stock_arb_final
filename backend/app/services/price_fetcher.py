import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
import yfinance as yf
from ..config import STOCKS, FETCH_INTERVAL
from ..redis_client import r

logger = logging.getLogger(__name__)
_executor = ThreadPoolExecutor(max_workers=4)


def _download_price(symbol: str) -> float | None:
    try:
        data = yf.download(symbol, period="1d", interval="1m", progress=False,
                           auto_adjust=True, multi_level_index=False)
        if not data.empty:
            return float(data["Close"].iloc[-1])
    except Exception as exc:
        logger.warning("yfinance fetch failed for %s: %s", symbol, exc)
    return None


async def fetch_stock(symbol: str) -> float | None:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, _download_price, symbol)


async def price_fetcher():
    while True:
        try:
            for nse, bse in STOCKS:
                nse_price = await fetch_stock(nse)
                bse_price = await fetch_stock(bse)
                if nse_price is not None:
                    await r.set(nse, nse_price)
                if bse_price is not None:
                    await r.set(bse, bse_price)
        except Exception as exc:
            logger.error("Price fetcher loop error: %s", exc)
        await asyncio.sleep(FETCH_INTERVAL)


def start_price_fetcher():
    asyncio.get_event_loop().create_task(price_fetcher())
