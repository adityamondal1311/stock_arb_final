from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.config import SYMBOLS
from app.price_fetcher import fetch_yahoo
from app.database import SessionLocal
from app.crud import save_price

async def fetch_all_prices():
    db = SessionLocal()
    for sym in SYMBOLS:
        nse = await fetch_yahoo(sym + ".NS")
        bse = await fetch_yahoo(sym + ".BO")
        if nse: await save_price(db, sym, "NSE", nse)
        if bse: await save_price(db, sym, "BSE", bse)
    await db.close()

def start_scheduler():
    sch = AsyncIOScheduler()
    sch.add_job(fetch_all_prices, "interval", minutes=1)
    sch.start()
