import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import prices, arbitrage, ws
from .services.price_fetcher import start_price_fetcher
from .services.arb_engine import start_arb_engine
from .database import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Stock Arbitrage Screener")

_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
_origins = [o.strip() for o in _raw_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prices.router)
app.include_router(arbitrage.router)
app.include_router(ws.router)


@app.on_event("startup")
async def startup():
    try:
        await init_db()
    except Exception as exc:
        logger.critical("Database init failed: %s", exc)
        raise
    try:
        start_price_fetcher()
        start_arb_engine()
    except Exception as exc:
        logger.critical("Background service startup failed: %s", exc)
        raise


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "ok"}
