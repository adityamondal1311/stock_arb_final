import asyncio
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..redis_client import r
from ..config import STOCKS

logger = logging.getLogger(__name__)
router = APIRouter()


@router.websocket("/ws/live")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket client connected")
    try:
        while True:
            keys = [sym for pair in STOCKS for sym in pair]
            values = await r.mget(keys)
            await websocket.send_json(dict(zip(keys, values)))
            await asyncio.sleep(30)
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as exc:
        logger.error("WebSocket error: %s", exc)
    finally:
        try:
            await websocket.close()
        except Exception:
            pass
