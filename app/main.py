from fastapi import FastAPI, Depends
from app.database import Base, engine, SessionLocal
from app.crud import get_latest_prices
from app.scheduler import start_scheduler, fetch_all_prices
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    start_scheduler()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/prices")
async def prices(db: AsyncSession = Depends(get_db)):
    return await get_latest_prices(db)

@app.get("/arbitrage")
async def arbitrage(db: AsyncSession = Depends(get_db)):
    rows = await get_latest_prices(db)
    arb = []
    by_sym = {}
    for r in rows:
        by_sym.setdefault(r.symbol, {})[r.exchange] = r.price
    for sym, data in by_sym.items():
        if "NSE" in data and "BSE" in data:
            diff = data["NSE"] - data["BSE"]
            arb.append({"symbol": sym, "diff": round(diff,2)})
    return arb

@app.post("/fetch-now")
async def fetch_now():
    await fetch_all_prices()
    return {"status": "done"}
