import logging
from pathlib import Path
import asyncpg
from .config import DB_URL

logger = logging.getLogger(__name__)
pool: asyncpg.Pool | None = None
_SCHEMA = (Path(__file__).parent / "init_schema.sql").read_text()


async def init_db():
    global pool
    pool = await asyncpg.create_pool(DB_URL, min_size=2, max_size=10)
    async with pool.acquire() as con:
        await con.execute(_SCHEMA)
    logger.info("Database pool ready, schema applied")


async def save_arbitrage(symbol: str, nse: float, bse: float, diff: float):
    async with pool.acquire() as con:
        await con.execute(
            """
            INSERT INTO arbitrage(symbol, nse_price, bse_price, difference)
            VALUES($1, $2, $3, $4)
            """,
            symbol, nse, bse, diff,
        )


async def fetch_latest() -> list[dict]:
    async with pool.acquire() as con:
        rows = await con.fetch(
            """
            SELECT id, symbol, nse_price, bse_price, difference,
                   timestamp AT TIME ZONE 'UTC' AS timestamp
            FROM arbitrage
            ORDER BY timestamp DESC
            LIMIT 20
            """
        )
        return [dict(row) for row in rows]
