import redis.asyncio as redis
from .config import REDIS_URL

redis = redis.from_url(REDIS_URL, decode_responses=True)
