import os

DB_URL = os.getenv("DB_URL", "postgresql://arbuser:secret@postgres:5432/arbdb")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
FETCH_INTERVAL = 2  # seconds
ARBITRAGE_THRESHOLD = 1  # Rs difference
STOCKS = [
    ("RELIANCE.NS", "RELIANCE.BO"),
    ("TCS.NS", "TCS.BO"),
    ("HDFCBANK.NS", "HDFCBANK.BO"),
]
