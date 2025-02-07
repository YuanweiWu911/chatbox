# app/cahce.py
from redis.asyncio import Redis
import json

class CacheManager:
    def __init__(self, redis_url):
        self.redis = Redis.from_url(redis_url)
    
    async def get(self, key: str):
        return await self.redis.get(f"chat:{key}")
    
    async def set(self, key: str, value: str, expire=3600):
        await self.redis.setex(f"chat:{key}", expire, value)
    
    async def close(self):
        await self.redis.close()
