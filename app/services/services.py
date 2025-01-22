import json
from abc import ABC, abstractmethod
from datetime import date, datetime

from fastapi import Depends
from services.cache_services import CacheTrade
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import config
from crud.spimex_trading import SpimexTradingCrud
from schemas import schemas


class Service(ABC):
    @abstractmethod
    def __init__(self, session: AsyncSession):
        pass

    @abstractmethod
    async def get_last_trading_dates(self, days_count: int):
        pass


class TradeService(Service):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.crud = SpimexTradingCrud(self.session)

    async def get_last_trading_dates(self, days_count: int):
        cache_key = f"last_trading_dates_{days_count}"
        cache_trade = CacheTrade(config.redis_url, cache_key)
        cached_data = await cache_trade.get_cache()
        if not cached_data:
            days = await self.crud.get_items_id(days_count)
            response = await self.date_to_string(days)
            new_cache = await cache_trade.set_cache(response)
            return await self.string_to_date(new_cache)

        return cached_data

    async def date_to_string(self, data: list):
        converter_data = [{"date": day.strftime("%Y-%m-%d")} for day in data]
        return json.dumps(converter_data)

    async def string_to_date(self, data: list):
        converter_data = [
            {"date": datetime.strptime(day["date"], "%Y-%m-%d").date()}
            for day in data
        ]
        return converter_data

    async def get_dynamics(
        self, params: schemas.TradingResultsParams = Depends()
    ):
        cache_key = (
            f"get_dynamics_{params.oil_id}_"
            f"{params.delivery_type_id}_"
            f"{params.delivery_basis_id}_"
            f"{params.start_date}_"  # type: ignore[attr-defined]
            f"{params.end_date}"  # type: ignore[attr-defined]
        )
        cache_trade = CacheTrade(config.redis_url, cache_key)
        cached_data = await cache_trade.get_cache()
        if not cached_data:
            data = params.model_dump(exclude_unset=True)
            data = {
                key: value for key, value in data.items() if value is not None
            }
            start_date = data.pop("start_date")
            end_date = data.pop("end_date")
            result = await self.crud.get_dynamics_params(
                start_date, end_date, data or None
            )
            response = await self.model_to_string(result)
            new_cache = await cache_trade.set_cache(response)
            return new_cache

        return cached_data

    async def model_to_string(self, data: list):
        converter_data = [field.to_dict() for field in data]
        for field in converter_data:
            for key, value in field.items():
                if isinstance(value, date):
                    field[key] = value.strftime("%Y-%m-%d")
        return json.dumps(converter_data)

    async def get_trading_results(
        self, params: schemas.TradingResultsParams = Depends()
    ):
        cache_key = (
            f"get_dynamics_{params.oil_id}_{params.delivery_type_id}_"
            f"{params.delivery_basis_id}"
        )
        cache_trade = CacheTrade(config.redis_url, cache_key)
        cached_data = await cache_trade.get_cache()
        if not cached_data:
            data = params.model_dump(exclude_unset=True)
            data = {
                key: value for key, value in data.items() if value is not None
            }
            result = await self.crud.get_trading_results_params(data or None)
            response = await self.model_to_string(result)
            new_cache = await cache_trade.set_cache(response)
            return new_cache

        return cached_data
