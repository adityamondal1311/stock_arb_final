import logging
import os
from contextlib import asynccontextmanager
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
    except Exception as exc:
        logger.critical("Database init failed: %s", exc)
        raise
    try:
        tasks = [start_price_fetcher(), start_arb_engine()]
    except Exception as exc:
        logger.critical("Background service startup failed: %s", exc)
        raise
    yield
    for task in tasks:
        task.cancel()


app = FastAPI(title="Stock Arbitrage Screener", lifespan=lifespan)

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


@app.get("/")
def root():
    return {"status": "ok"}


@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    return {"status": "ok"}
