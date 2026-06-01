import logging
from fastapi import APIRouter, HTTPException
from ..database import fetch_latest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/arbitrage", tags=["Arbitrage"])


@router.get("/latest")
async def latest_arbitrage():
    try:
        return await fetch_latest()
    except Exception as exc:
        logger.error("Failed to fetch arbitrage records: %s", exc)
        raise HTTPException(status_code=503, detail="Arbitrage data unavailable")
