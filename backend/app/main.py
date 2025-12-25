from fastapi import FastAPI
from .routers import prices, arbitrage, ws
from .services.price_fetcher import start_price_fetcher
from .services.arb_engine import start_arb_engine
from .database import init_db

app = FastAPI()

app.include_router(prices.router)
app.include_router(arbitrage.router)
app.include_router(ws.router)

@app.on_event("startup")
async def startup():
    await init_db()
    start_price_fetcher()
    start_arb_engine()

@app.get("/")
def root():
    return {"status": "Stock Arbitrage Screener Running"}
