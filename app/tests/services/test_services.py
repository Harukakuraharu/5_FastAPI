from datetime import date, datetime

import pytest
from services import services

from schemas import schemas
from tests import factory as fc


pytestmark = pytest.mark.anyio


async def test_get_last_trading_dates(async_session, factory):
    """
    Test for get last trading dates
    """
    count = 5
    await factory(fc.TradeFactory, count)
    result = await services.TradeService(async_session).get_last_trading_dates(
        5
    )
    assert len(result) == count
    for day in result:
        assert isinstance(day["date"], date)


async def test_get_dynamics_oil_id(async_session, factory):
    """
    Test get dynamics with filter oil_id
    """
    params = schemas.DynamicsParams(
        oil_id="Hehehe",
        start_date="2023-01-01",
        end_date="2023-01-10",
    )
    count = 2
    date_1 = datetime.strptime("2023-01-02", "%Y-%m-%d").date()
    await factory(fc.TradeFactory, count, oil_id="Hehehe", date=date_1)
    await factory(fc.TradeFactory, 5)
    result = await services.TradeService(async_session).get_dynamics(params)
    assert len(result) == count


async def test_get_dynamics(async_session, factory):
    """
    Test get dynamics with only date
    """
    params = schemas.DynamicsParams(
        start_date="2023-01-01",
        end_date="2023-01-10",
    )
    count = 2
    date_1 = datetime.strptime("2023-01-02", "%Y-%m-%d").date()
    await factory(fc.TradeFactory, count, date=date_1)
    await factory(fc.TradeFactory, 5)
    result = await services.TradeService(async_session).get_dynamics(params)
    assert len(result) == count


async def test_get_trading_results(async_session, factory):
    """
    Test get trading result
    """
    params = schemas.TradingResultsParams(oil_id="Hehehe")
    date_1 = datetime.strptime("2023-01-02", "%Y-%m-%d").date()
    date_last = datetime.strptime("2023-05-06", "%Y-%m-%d").date()
    await factory(fc.TradeFactory, 3, date=date_1)
    await factory(fc.TradeFactory, date=date_last, oil_id="Hehehe")
    result = await services.TradeService(async_session).get_trading_results(
        params
    )
    assert len(result) == 1
    assert result[0]["date"] == "2023-05-06"
