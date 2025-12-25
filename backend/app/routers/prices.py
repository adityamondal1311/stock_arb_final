from fastapi import APIRouter
from ..redis_client import redis
from ..config import STOCKS

router = APIRouter(prefix="/prices", tags=["Prices"])

@router.get("/live")
async def get_prices():
    data = {}
    for nse, bse in STOCKS:
        data[nse] = await redis.get(nse)
        data[bse] = await redis.get(bse)
    return data
