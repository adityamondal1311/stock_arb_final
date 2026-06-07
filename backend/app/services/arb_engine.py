import asyncio
import logging
from ..config import STOCKS, ARBITRAGE_THRESHOLD
from ..redis_client import r
from ..database import save_arbitrage

logger = logging.getLogger(__name__)


async def arbitrage_engine():
    while True:
        try:
            for nse, bse in STOCKS:
                p1 = await r.get(nse)
                p2 = await r.get(bse)

                if p1 is None or p2 is None:
                    continue

                p1, p2 = float(p1), float(p2)
                diff = abs(p1 - p2)

                if diff >= ARBITRAGE_THRESHOLD:
                    symbol = nse.replace(".NS", "")
                    await save_arbitrage(symbol, p1, p2, diff)
        except Exception as exc:
            logger.error("Arbitrage engine loop error: %s", exc)
        await asyncio.sleep(30)


def start_arb_engine():
    asyncio.get_event_loop().create_task(arbitrage_engine())
