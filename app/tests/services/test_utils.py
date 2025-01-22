import json
from datetime import date

import pytest
from services import utils

from tests import factory as fc


pytestmark = pytest.mark.anyio


async def test_model_to_string(factory):
    """Test converter model object on string for set in cache"""
    data = await factory(fc.TradeFactory, 2)
    result = await utils.model_to_string(data)
    assert isinstance(result, str)
    result_list = json.loads(result)
    assert isinstance(result_list, list)


async def test_date_to_string():
    """Test converter datetime type on string for set in cache"""
    data = await fc.UtilsFactory().generate_data_to_string()
    result = await utils.date_to_string(data)
    assert isinstance(result, str)
    result_list = json.loads(result)
    assert isinstance(result_list, list)


async def test_string_to_date():
    """Test converter date with string type on date format"""
    data = await fc.UtilsFactory().generate_data_to_date()
    result = await utils.string_to_date(data)
    assert isinstance(result, list)
    for day in result:
        assert isinstance(day["date"], date)
