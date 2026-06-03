# ArbScreen — NSE/BSE Real-Time Arbitrage Screener

> A live arbitrage screener that detects price gaps between the NSE and BSE for Indian large-cap stocks. Built with FastAPI, React, WebSocket, Redis, and PostgreSQL.

🔗 **Live Demo:** [stock-arb-final.vercel.app](https://stock-arb-final.vercel.app)

---

## What It Does

Indian stocks listed on both the NSE and BSE occasionally trade at different prices simultaneously. ArbScreen monitors three large-cap stocks — Reliance, TCS, and HDFC Bank — in real time, detects spreads ≥ ₹1 between exchanges, persists every gap to a database, and streams live prices to the browser over WebSocket.

> Prices are ~15 minutes delayed (yfinance free tier). Real-time data would require a broker API such as Zerodha Kite Connect or Upstox.

---

## Architecture

```
Frontend (React + Vite)  ──WebSocket──▶  Backend (FastAPI)
        │                                      │
   Vercel CDN                        ┌─────────┴─────────┐
                                  Redis             PostgreSQL
                                (Upstash)           (Supabase)
                                    ↑                    ↑
                             price_fetcher.py      arb_engine.py
                             (every 30s)           (every 1s)
```

The backend runs two async background services. The price fetcher pulls NSE and BSE prices from yfinance every 30 seconds and writes them to Redis. The arbitrage engine reads Redis every second, computes spreads, and persists any gap above the threshold to Postgres. The WebSocket endpoint reads Redis and pushes current prices to all connected clients every second.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite 4, Tailwind CSS v3 |
| Backend | FastAPI, Python 3.10, uvicorn |
| Cache | Redis via redis.asyncio (Upstash) |
| Database | PostgreSQL via asyncpg (Supabase) |
| Price data | yfinance v1.0 |
| Containers | Docker |
| Hosting | Vercel (frontend) + Render (backend) |

---

## Backend Services

| Service | File | Description |
|---|---|---|
| Price fetcher | `price_fetcher.py` | Fetches NSE and BSE prices every 30s in a `ThreadPoolExecutor` (yfinance is synchronous), writes to Redis |
| Arbitrage engine | `arb_engine.py` | Reads Redis every 1s, detects spreads ≥ threshold, persists to Postgres |
| WebSocket | `ws.py` | Pushes live prices to all connected clients every 1s with disconnect-safe cleanup |

---

## API

| Method | Path | Description |
|---|---|---|
| GET | `/` | Status |
| GET / HEAD | `/health` | Health check |
| GET | `/prices/live` | Current prices from Redis |
| GET | `/arbitrage/latest` | Last 20 arbitrage records from Postgres |
| WS | `/ws/live` | Live price stream |

---

## UI Features

- Sticky header with live/connecting/reconnecting/disconnected status badge (pulsing dot)
- Live Prices table — NSE and BSE columns side by side, color flash on price update, spread badge
- Arbitrage Opportunities panel — spread badges colored by size (green < ₹2, amber ≥ ₹2, red ≥ ₹5), direction label (NSE > BSE), skeleton loader, empty state
- WebSocket client with exponential backoff reconnection (8 retries)
- 15-minute delay disclaimer visible in the header

---

## Running Locally

**Prerequisites:** Docker + Docker Compose

```bash
cp .env.example .env
# fill in DB_URL and REDIS_URL
docker compose up --build
```

Frontend: http://localhost:5173  
Backend: http://localhost:8000

---

## Environment Variables

### Backend

| Variable | Description | Default |
|---|---|---|
| `DB_URL` | PostgreSQL connection string | required |
| `REDIS_URL` | Redis connection string (`rediss://`) | required |
| `FETCH_INTERVAL` | Price fetch interval in seconds | `30` |
| `ARBITRAGE_THRESHOLD` | Minimum spread to record (₹) | `1` |
| `ALLOWED_ORIGINS` | Comma-separated CORS origins | `http://localhost:5173` |

### Frontend

| Variable | Description |
|---|---|
| `VITE_API_URL` | Backend URL |

---

## Deployment

| Service | Provider | Notes |
|---|---|---|
| Frontend | Vercel | Root directory: `frontend` |
| Backend | Render | Root directory: `backend`, Docker, free tier |
| Database | Supabase | Session pooler on port 5432 (IPv4 compatible) |
| Cache | Upstash | `rediss://` TLS required |
| Keep-alive | UptimeRobot | Pings `/health` every 5 minutes to prevent Render sleep |

---

## Project Structure

```
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py               # FastAPI app, CORS, startup lifecycle
│       ├── config.py             # Env var loading
│       ├── database.py           # asyncpg pool, schema init
│       ├── redis_client.py       # aioredis client
│       ├── init_schema.sql
│       ├── routers/
│       │   ├── prices.py
│       │   ├── arbitrage.py
│       │   └── ws.py
│       └── services/
│           ├── price_fetcher.py
│           └── arb_engine.py
└── frontend/
    └── src/
        ├── App.jsx
        ├── websocket.js          # WS client, exponential backoff
        ├── useWsStatus.js        # live/connecting/reconnecting/disconnected hook
        └── components/
            ├── LivePricesTable.jsx
            └── ArbitragePanel.jsx
```

---

## Design Decisions

**Why Redis between the fetcher and the WebSocket layer?**  
yfinance is synchronous and takes 1-2 seconds per fetch. Decoupling price fetching from the WebSocket broadcast via Redis means WebSocket clients always get an instant response from cache — they are never blocked waiting on yfinance. The fetcher and the WebSocket layer run on independent clocks.

**Why `ThreadPoolExecutor` for yfinance?**  
FastAPI runs on an async event loop. A blocking synchronous call like yfinance inside a coroutine would stall the entire event loop and make the API unresponsive. Offloading it to a thread pool via `run_in_executor` keeps the async loop free while yfinance does its work on a separate thread.

**Why Supabase Session pooler instead of Transaction pooler?**  
Render's free tier uses IPv4 only. Supabase's Transaction pooler uses IPv6 by default. The Session pooler is IPv4-compatible and maintains persistent connections — the right choice for a long-running FastAPI server with a connection pool.

**Why asyncpg `statement_cache_size=0`?**  
asyncpg caches prepared statements by default. pgBouncer in session mode does not preserve connection state across client sessions the same way a raw Postgres connection does. Setting `statement_cache_size=0` disables prepared statement caching and prevents cache invalidation errors under the pooler.
