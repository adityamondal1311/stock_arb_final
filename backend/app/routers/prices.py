import logging
from fastapi import APIRouter, HTTPException
from ..redis_client import r
from ..config import STOCKS

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("/live")
async def get_prices():
    try:
        data = {}
        for nse, bse in STOCKS:
            data[nse] = await r.get(nse)
            data[bse] = await r.get(bse)
        return data
    except Exception as exc:
        logger.error("Failed to fetch prices: %s", exc)
        raise HTTPException(status_code=503, detail="Price data unavailable")
