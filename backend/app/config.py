import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.environ["DB_URL"]
REDIS_URL = os.environ["REDIS_URL"]
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", "30"))
ARBITRAGE_THRESHOLD = float(os.getenv("ARBITRAGE_THRESHOLD", "1"))

STOCKS = [
    ("RELIANCE.NS", "RELIANCE.BO"),
    ("TCS.NS", "TCS.BO"),
    ("HDFCBANK.NS", "HDFCBANK.BO"),
]
