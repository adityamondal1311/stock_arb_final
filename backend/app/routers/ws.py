from fastapi import APIRouter, WebSocket
from ..redis_client import redis
import asyncio
from ..config import STOCKS

router = APIRouter()

@router.websocket("/ws/live")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()

    while True:
        result = {}
        for nse, bse in STOCKS:
            result[nse] = await redis.get(nse)
            result[bse] = await redis.get(bse)

        await websocket.send_json(result)
        await asyncio.sleep(1)
