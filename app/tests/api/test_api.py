from datetime import datetime

import pytest
from fastapi import status

from tests import factory as fc


pytestmark = pytest.mark.anyio


async def test_get_last_trading_dates(client, factory):
    """Test for get last dates in /spimex/get_last_trading_dates"""
    days_count = 5
    await factory(fc.TradeFactory, 10)
    response = await client.get(
        "/spimex/get_last_trading_dates", params={"days_count": days_count}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == days_count


async def test_check_last_trading_dates(client, factory):
    """Test for check correct last date in /spimex/get_last_trading_dates"""
    days_count = 2
    data = await factory(fc.TradeFactory, 5)
    response = await client.get(
        "/spimex/get_last_trading_dates", params={"days_count": days_count}
    )
    assert response.status_code == status.HTTP_200_OK
    date = [item.date for item in data]
    date.sort(reverse=True)
    result = [{"date": day.strftime("%Y-%m-%d")} for day in date[:2]]
    assert result == response.json()


async def test_get_dynamics_oil_id(client, factory):
    """
    Test for get dynamics trade with filter oil_id on /spimex/get_dynamics
    """
    date_1 = datetime.strptime("2023-01-02", "%Y-%m-%d").date()
    date_2 = datetime.strptime("2023-01-05", "%Y-%m-%d").date()
    param_filter = "Hahaha"
    await factory(fc.TradeFactory, 5, oil_id=param_filter, date=date_1)
    await factory(fc.TradeFactory, 3, oil_id=param_filter, date=date_2)
    await factory(fc.TradeFactory, 3, oil_id="Hehehe", date=date_2)
    response = await client.get(
        "/spimex/get_dynamics",
        params={
            "oil_id": param_filter,
            "start_date": "2023-01-01",
            "end_date": "2023-01-10",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 8


async def test_get_dynamics_delivery_type_id(client, factory):
    """
    Test for get dynamics trade with filter delivery_type_id
    on /spimex/get_dynamics
    """
    date_1 = datetime.strptime("2023-01-02", "%Y-%m-%d").date()
    date_2 = datetime.strptime("2023-01-05", "%Y-%m-%d").date()
    await factory(fc.TradeFactory, 2, delivery_type_id="Hehe", date=date_1)
    await factory(fc.TradeFactory, 3, delivery_type_id="oooooooo", date=date_1)
    await factory(fc.TradeFactory, 5, delivery_type_id="Hehe", date=date_2)
    response = await client.get(
        "/spimex/get_dynamics",
        params={
            "delivery_type_id": "Hehe",
            "start_date": "2023-01-01",
            "end_date": "2023-01-10",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 7


async def test_get_dynamics_all_filters(client, factory):
    """
    Test for get dynamics trade with all_filters on /spimex/get_dynamics
    """
    delivery_basis_id = "11111"
    delivery_type_id = "22222"
    oil_id = "33333"
    date_1 = datetime.strptime("2023-01-02", "%Y-%m-%d").date()
    await factory(
        fc.TradeFactory,
        2,
        delivery_type_id=delivery_type_id,
        oil_id=oil_id,
        delivery_basis_id=delivery_basis_id,
        date=date_1,
    )
    await factory(
        fc.TradeFactory,
        2,
        delivery_type_id="ooooooo",
        oil_id=oil_id,
        delivery_basis_id=delivery_basis_id,
        date=date_1,
    )
    response = await client.get(
        "/spimex/get_dynamics",
        params={
            "oil_id": oil_id,
            "delivery_type_id": delivery_type_id,
            "delivery_basis_id": delivery_basis_id,
            "start_date": "2023-01-01",
            "end_date": "2023-01-10",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2


async def test_get_trading_results_params(client, factory):
    """
    Test for get dynamics trade with all_filters on /spimex/get_trading_results
    """
    delivery_basis_id = "5555"
    delivery_type_id = "66666"
    oil_id = "7777"
    count = 5
    date_1 = datetime.strptime("2023-01-02", "%Y-%m-%d").date()
    date_2 = datetime.strptime("2023-01-08", "%Y-%m-%d").date()
    await factory(
        fc.TradeFactory,
        2,
        delivery_type_id=delivery_type_id,
        oil_id=oil_id,
        delivery_basis_id=delivery_basis_id,
        date=date_1,
    )
    await factory(
        fc.TradeFactory,
        count,
        delivery_type_id=delivery_type_id,
        oil_id=oil_id,
        delivery_basis_id=delivery_basis_id,
        date=date_2,
    )
    response = await client.get(
        "/spimex/get_trading_results",
        params={
            "oil_id": oil_id,
            "delivery_type_id": delivery_type_id,
            "delivery_basis_id": delivery_basis_id,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == count
