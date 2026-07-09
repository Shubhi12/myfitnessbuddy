import json
from typing import Any

from app.application.interfaces.cache_service import CacheService
from app.infrastructure.cache.redis_client import get_redis_client


class RedisCacheService(CacheService):
    async def get(self, key: str) -> Any | None:
        client = await get_redis_client()
        value = await client.get(key)
        if value is None:
            return None
        return json.loads(value)

    async def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        client = await get_redis_client()
        await client.setex(key, ttl_seconds, json.dumps(value, default=str))

    async def delete(self, key: str) -> None:
        client = await get_redis_client()
        await client.delete(key)

    async def invalidate_pattern(self, pattern: str) -> None:
        client = await get_redis_client()
        keys = await client.keys(pattern)
        if keys:
            await client.delete(*keys)
