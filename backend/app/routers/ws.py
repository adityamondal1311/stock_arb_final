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
            result = {}
            for nse, bse in STOCKS:
                result[nse] = await r.get(nse)
                if bse is not None:
                    result[bse] = await r.get(bse)
            await websocket.send_json(result)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as exc:
        logger.error("WebSocket error: %s", exc)
    finally:
        try:
            await websocket.close()
        except Exception:
            pass
