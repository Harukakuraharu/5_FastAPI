import json

import pytest
from services.cache_services import redis_client

from tests.factory import CacheFactory


pytestmark = pytest.mark.anyio


@pytest.mark.parametrize("cache_key", [("test"), ("123456")])
async def test_set_data_redis(cache_key):
    """Test for set cache in Redis"""
    data = await CacheFactory().generate_data()
    redis_client.set(cache_key, data, ex=100)
    assert redis_client.get(cache_key) is not None


@pytest.mark.parametrize(
    "cache_key, result", [("test", True), ("test2", False)]
)
async def test_get_data(cache_key, result):
    """Test for get data in Redis"""
    data = await CacheFactory().generate_data()
    redis_client.set("test", data, ex=100)
    response = redis_client.get(cache_key)
    data = await CacheFactory().generate_data()
    if result:
        assert json.loads(response) == json.loads(data)
    else:
        assert response is None
