import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
import yfinance as yf
from ..config import STOCKS, FETCH_INTERVAL
from ..redis_client import r

logger = logging.getLogger(__name__)
_executor = ThreadPoolExecutor(max_workers=4)


def _batch_download(symbols: list[str]) -> dict[str, float]:
    ticker_str = " ".join(symbols)
    for attempt in range(2):
        try:
            data = yf.download(ticker_str, period="1d", interval="1m", progress=False,
                               auto_adjust=True, multi_level_index=False)
            if data.empty:
                logger.warning("Empty batch response on attempt %d", attempt + 1)
                continue
            prices = {}
            for sym in symbols:
                col = f"Close_{sym}"
                if col in data.columns:
                    val = data[col].dropna()
                    if not val.empty:
                        prices[sym] = float(val.iloc[-1])
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
            nse_prices, bse_prices = await asyncio.gather(
                loop.run_in_executor(_executor, _batch_download, nse_symbols),
                loop.run_in_executor(_executor, _batch_download, bse_symbols),
            )
            all_prices = {**nse_prices, **bse_prices}
            if all_prices:
                for symbol, price in all_prices.items():
                    await r.set(symbol, price)
            else:
                logger.warning("No prices returned from either batch — skipping Redis update")
        except Exception as exc:
            logger.error("Price fetcher loop error: %s", exc)
        await asyncio.sleep(FETCH_INTERVAL)


def start_price_fetcher():
    asyncio.get_event_loop().create_task(price_fetcher())
