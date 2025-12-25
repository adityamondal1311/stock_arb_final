import asyncio
from ..config import STOCKS, ARBITRAGE_THRESHOLD
from ..redis_client import redis
from ..database import save_arbitrage

async def arbitrage_engine():
    while True:
        for nse, bse in STOCKS:
            p1 = await redis.get(nse)
            p2 = await redis.get(bse)

            if not p1 or not p2:
                continue

            p1, p2 = float(p1), float(p2)
            diff = abs(p1 - p2)

            if diff >= ARBITRAGE_THRESHOLD:
                symbol = nse.replace(".NS", "")
                await save_arbitrage(symbol, p1, p2, diff)

        await asyncio.sleep(1)

def start_arb_engine():
    asyncio.get_event_loop().create_task(arbitrage_engine())
