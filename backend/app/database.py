import asyncpg
from .config import DB_URL
import asyncio

pool = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool(DB_URL)

async def save_arbitrage(symbol, nse, bse, diff):
    async with pool.acquire() as con:
        await con.execute("""
            INSERT INTO arbitrage(symbol, nse_price, bse_price, difference)
            VALUES($1, $2, $3, $4)
        """, symbol, nse, bse, diff)

async def fetch_latest():
    async with pool.acquire() as con:
        rows = await con.fetch("""
            SELECT * FROM arbitrage
            ORDER BY timestamp DESC
            LIMIT 20
        """)
        return [dict(r) for r in rows]
