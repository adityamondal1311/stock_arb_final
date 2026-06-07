import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
import yfinance as yf
from ..config import STOCKS, FETCH_INTERVAL
from ..redis_client import r

logger = logging.getLogger(__name__)
_executor = ThreadPoolExecutor(max_workers=10)

_BATCH_SIZE = 10


def _chunked(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def _batch_download(symbols: list[str]) -> dict[str, float]:
    ticker_str = " ".join(symbols)
    for attempt in range(2):
        try:
            data = yf.download(ticker_str, period="5d", interval="1d", progress=False,
                               auto_adjust=True, multi_level_index=False)
            if data.empty:
                logger.warning("Empty batch response on attempt %d (first: %s)", attempt + 1, symbols[0])
                continue
            prices = {}
            for sym in symbols:
                # Single-symbol download returns plain "Close"; multi-symbol returns "Close_SYM"
                col = "Close" if len(symbols) == 1 else f"Close_{sym}"
                if col in data.columns:
                    val = data[col].dropna()
                    if not val.empty:
                        prices[sym] = float(val.iloc[-1])
            logger.info("Batch result for %s…: %d/%d prices fetched", symbols[:3], len(prices), len(symbols))
            return prices
        except Exception as exc:
            logger.warning("Batch download attempt %d failed: %s", attempt + 1, exc)
    return {}


async def price_fetcher():
    while True:
        try:
            nse_symbols = [nse for nse, _ in STOCKS]
            bse_symbols = [bse for _, bse in STOCKS]
            loop = asyncio.get_event_loop()

            tasks = [
                loop.run_in_executor(_executor, _batch_download, chunk)
                for chunk in _chunked(nse_symbols, _BATCH_SIZE)
            ] + [
                loop.run_in_executor(_executor, _batch_download, chunk)
                for chunk in _chunked(bse_symbols, _BATCH_SIZE)
            ]

            results = await asyncio.gather(*tasks)
            all_prices = {}
            for chunk_prices in results:
                all_prices.update(chunk_prices)

            if all_prices:
                for symbol, price in all_prices.items():
                    await r.set(symbol, price)
            else:
                logger.warning("No prices returned from any batch — skipping Redis update")
        except Exception as exc:
            logger.error("Price fetcher loop error: %s", exc)
        await asyncio.sleep(FETCH_INTERVAL)


def start_price_fetcher():
    asyncio.get_event_loop().create_task(price_fetcher())
