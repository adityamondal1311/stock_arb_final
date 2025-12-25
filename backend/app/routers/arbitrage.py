from fastapi import APIRouter
from ..database import fetch_latest

router = APIRouter(prefix="/arbitrage", tags=["Arbitrage"])

@router.get("/latest")
async def latest_arbitrage():
    return await fetch_latest()
