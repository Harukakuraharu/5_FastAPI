# from cache_fastapi.cacheMiddleware import (  # type: ignore[import-untyped]
#     CacheMiddleware,
# )
from fastapi import FastAPI

from api.api import spimex_routers
# from core.redis_cli import RedisBackend
from services.cache_services import redis_client

app = FastAPI()


app.include_router(spimex_routers)
