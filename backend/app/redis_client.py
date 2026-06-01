import redis.asyncio as aioredis
from .config import REDIS_URL

r = aioredis.from_url(REDIS_URL, decode_responses=True)
