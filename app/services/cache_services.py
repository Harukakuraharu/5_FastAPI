import json

import redis

from core.settings import config


redis_client = redis.Redis().from_url(config.redis_url)  # type: ignore


class CacheTrade:
    def __init__(self, redis_url, cache_key):
        self.redis_client = redis.Redis().from_url(redis_url)
        self.cache_key = cache_key

    async def get_cache(self):
        cached_data = self.redis_client.get(self.cache_key)
        if cached_data:
            return json.loads(cached_data)

    async def set_cache(self, data):
        self.redis_client.set(self.cache_key, data)
        return json.loads(data)
