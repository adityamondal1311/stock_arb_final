from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Base, engine, SessionLocal
from app.crud import get_latest_prices, save_price
from app.scheduler import start_scheduler, fetch_all_prices

app = FastAPI(title="Stock Arbitrage Screener")

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

# Startup event: create tables + start scheduler
@app.on_event("startup")
async def startup():
    # Create tables if not exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Start the periodic scheduler (fetches prices every 1 min)
    start_scheduler()

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}

# Get latest stored prices
@app.get("/prices")
async def prices(db: AsyncSession = Depends(get_db)):
    try:
        rows = await get_latest_prices(db)
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get simple arbitrage differences (NSE - BSE)
@app.get("/arbitrage")
async def arbitrage(db: AsyncSession = Depends(get_db)):
    try:
        rows = await get_latest_prices(db)
        arb = []
        by_sym = {}
        for r in rows:
            by_sym.setdefault(r.symbol, {})[r.exchange] = r.price
        for sym, data in by_sym.items():
            if "NSE" in data and "BSE" in data:
                diff = data["NSE"] - data["BSE"]
                arb.append({"symbol": sym, "diff": round(diff, 2)})
        return arb
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Manually trigger price fetch
@app.post("/fetch-now")
async def fetch_now():
    try:
        await fetch_all_prices()
        return {"status": "done"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
