import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.environ["DB_URL"]
REDIS_URL = os.environ["REDIS_URL"]
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", "30"))
ARBITRAGE_THRESHOLD = float(os.getenv("ARBITRAGE_THRESHOLD", "1"))

STOCKS = [
    ("ADANIENT.NS",   None),             # ADANIENT.BO not on Yahoo Finance
    ("ADANIPORTS.NS", None),             # ADANIPORTS.BO not on Yahoo Finance
    ("APOLLOHOSP.NS", "APOLLOHOSP.BO"),
    ("ASIANPAINT.NS", "ASIANPAINT.BO"),
    ("AXISBANK.NS",   "AXISBANK.BO"),
    ("BAJAJ-AUTO.NS", "BAJAJ-AUTO.BO"),
    ("BAJAJFINSV.NS", "BAJAJFINSV.BO"),
    ("BAJFINANCE.NS", "BAJFINANCE.BO"),
    ("BEL.NS",        "BEL.BO"),
    ("BHARTIARTL.NS", None),             # BHARTIARTL.BO not on Yahoo Finance
    ("BPCL.NS",       None),             # BPCL.BO not on Yahoo Finance
    ("BRITANNIA.NS",  "BRITANNIA.BO"),
    ("CIPLA.NS",      "CIPLA.BO"),
    ("COALINDIA.NS",  None),             # COALINDIA.BO not on Yahoo Finance
    ("DIVISLAB.NS",   "DIVISLAB.BO"),
    ("DRREDDY.NS",    "DRREDDY.BO"),
    ("EICHERMOT.NS",  "EICHERMOT.BO"),
    ("GRASIM.NS",     "GRASIM.BO"),
    ("HCLTECH.NS",    "HCLTECH.BO"),
    ("HDFCBANK.NS",   "HDFCBANK.BO"),
    ("HDFCLIFE.NS",   "HDFCLIFE.BO"),
    ("HEROMOTOCO.NS", "HEROMOTOCO.BO"),
    ("HINDALCO.NS",   "HINDALCO.BO"),
    ("HINDUNILVR.NS", "HINDUNILVR.BO"),
    ("ICICIBANK.NS",  "ICICIBANK.BO"),
    ("INDUSINDBK.NS", "INDUSINDBK.BO"),
    ("INFY.NS",       "INFY.BO"),
    ("ITC.NS",        "ITC.BO"),
    ("JSWSTEEL.NS",   "JSWSTEEL.BO"),
    ("KOTAKBANK.NS",  "KOTAKBANK.BO"),
    ("LT.NS",         "LT.BO"),
    ("M&M.NS",        "M&M.BO"),
    ("MARUTI.NS",     "MARUTI.BO"),
    ("NESTLEIND.NS",  "NESTLEIND.BO"),
    ("NTPC.NS",       None),             # NTPC.BO not on Yahoo Finance
    ("ONGC.NS",       None),             # ONGC.BO not on Yahoo Finance
    ("POWERGRID.NS",  None),             # POWERGRID.BO not on Yahoo Finance
    ("RELIANCE.NS",   "RELIANCE.BO"),
    ("SBIN.NS",       "SBIN.BO"),
    ("SHRIRAMFIN.NS", "SHRIRAMFIN.BO"),
    ("SUNPHARMA.NS",  "SUNPHARMA.BO"),
    ("TATAMOTORS.NS", None),             # TATAMOTORS.BO not on Yahoo Finance
    ("TATASTEEL.NS",  "TATASTEEL.BO"),
    ("TCS.NS",        "TCS.BO"),
    ("TECHM.NS",      "TECHM.BO"),
    ("TITAN.NS",      "TITAN.BO"),
    ("TATACONSUM.NS", "TATACONSUM.BO"),
    ("TRENT.NS",      "TRENT.BO"),
    ("ULTRACEMCO.NS", "ULTRACEMCO.BO"),
    ("WIPRO.NS",      "WIPRO.BO"),
]
