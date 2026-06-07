import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
import requests
import yfinance as yf
from ..config import STOCKS, FETCH_INTERVAL, BSE_SCRIP_CODES
from ..redis_client import r

logger = logging.getLogger(__name__)
_executor = ThreadPoolExecutor(max_workers=10)

_BATCH_SIZE = 10

_bse_session = requests.Session()
_bse_session.headers.update({
    "Referer": "https://www.bseindia.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
})


def _chunked(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def _batch_download(symbols: list[str]) -> dict[str, float]:
    ticker_str = " ".join(symbols)
    for attempt in range(2):
        try:
            data = yf.download(ticker_str, period="5d", interval="1d", progress=False,
                               auto_adjust=True)
            if data.empty:
                logger.warning("Empty batch response on attempt %d (first: %s)", attempt + 1, symbols[0])
                continue
            prices = {}
            for sym in symbols:
                try:
                    col = ("Close", sym)
                    if col in data.columns:
                        val = data[col].dropna()
                        if not val.empty:
                            prices[sym] = float(val.iloc[-1])
                except Exception as e:
                    logger.warning("Price extraction failed for %s: %s", sym, e)
            logger.info("NSE batch %s…: %d/%d fetched", symbols[:3], len(prices), len(symbols))
            return prices
        except Exception as exc:
            logger.warning("NSE batch attempt %d failed: %s", attempt + 1, exc)
    return {}


def _fetch_bse_price(bse_symbol: str) -> tuple[str, float | None]:
    scrip_code = BSE_SCRIP_CODES.get(bse_symbol)
    if not scrip_code:
        return bse_symbol, None
    try:
        url = (
            "https://api.bseindia.com/BseIndiaAPI/api/getScripHeaderData/w"
            f"?Debtflag=&scripcode={scrip_code}&seriesid="
        )
        resp = _bse_session.get(url, timeout=10)
        resp.raise_for_status()
        ltp = resp.json()["CurrRate"]["LTP"]
        return bse_symbol, float(ltp.replace(",", ""))
    except Exception as exc:
        logger.warning("BSE fetch failed for %s: %s", bse_symbol, exc)
        return bse_symbol, None


async def price_fetcher():
    while True:
        try:
            nse_symbols = [nse for nse, _ in STOCKS]
            bse_symbols = [bse for _, bse in STOCKS]
            loop = asyncio.get_event_loop()

            nse_tasks = [
                loop.run_in_executor(_executor, _batch_download, chunk)
                for chunk in _chunked(nse_symbols, _BATCH_SIZE)
            ]
            bse_tasks = [
                loop.run_in_executor(_executor, _fetch_bse_price, sym)
                for sym in bse_symbols
            ]

            nse_results, bse_results = await asyncio.gather(
                asyncio.gather(*nse_tasks),
                asyncio.gather(*bse_tasks),
            )

            all_prices = {}
            for chunk_prices in nse_results:
                all_prices.update(chunk_prices)
            for sym, price in bse_results:
                if price is not None:
                    all_prices[sym] = price

            if all_prices:
                for symbol, price in all_prices.items():
                    await r.set(symbol, price)
            else:
                logger.warning("No prices returned from any source — skipping Redis update")
        except Exception as exc:
            logger.error("Price fetcher loop error: %s", exc)
        await asyncio.sleep(FETCH_INTERVAL)


def start_price_fetcher():
    asyncio.get_event_loop().create_task(price_fetcher())
