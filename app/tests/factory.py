import json
from datetime import datetime
from typing import Any, Sequence

import sqlalchemy as sa
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

import models


faker = Faker()


class MainFactory:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.data: list[dict] = []
        self.model: models.TypeModel | None = None

    async def generate_data(self, count: int = 1, **kwargs):
        """
        Generate data for factory
        """
        raise NotImplementedError("Нужна реализация")

    async def insert_to_db(self) -> None:
        """
        Запись данных в БД
        """
        stmt = sa.insert(self.model).values(self.data)  # type:ignore[arg-type]
        await self.session.execute(stmt)

    async def get_data(self) -> Sequence[Any]:
        """
        Get data in DB
        """
        stmt = sa.select(self.model)  # type:ignore[arg-type]
        result = await self.session.scalars(stmt)
        return result.unique().all()


class TradeFactory(MainFactory):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = models.SpimexTradingResults

    async def generate_data(
        self, count: int = 1, **kwargs
    ) -> Sequence[models.SpimexTradingResults]:
        self.data.extend(
            {
                "exchange_product_id": kwargs.get(
                    "exchange_product_id", faker.name()
                ),
                "exchange_product_name": kwargs.get(
                    "exchange_product_name", faker.name()
                ),
                "oil_id": kwargs.get("oil_id", faker.name()),
                "delivery_basis_id": kwargs.get(
                    "delivery_basis_id", faker.name()
                ),
                "delivery_basis_name": kwargs.get(
                    "delivery_basis_name", faker.name()
                ),
                "delivery_type_id": kwargs.get(
                    "delivery_type_id", faker.name()
                ),
                "volume": kwargs.get("volume", faker.name()),
                "total": kwargs.get("total", faker.name()),
                "count": kwargs.get("count", faker.name()),
                "date": kwargs.get(
                    "date", datetime.strptime(faker.date(), "%Y-%m-%d").date()
                ),
            }
            for _ in range(count)
        )

        await self.insert_to_db()
        await self.session.commit()
        return await self.get_data()


class CacheFactory:
    async def generate_data(self):
        return json.dumps({"hello": "world", "привет": "мир"})


class UtilsFactory:
    async def generate_data_to_string(self):
        result = [
            datetime.strptime(f"2023-01-0{day+1}", "%Y-%m-%d").date()
            for day in range(5)
        ]
        return result

    async def generate_data_to_date(self):
        date_string = [{"date": f"2025-01-0{day+1}"} for day in range(5)]
        return date_string
