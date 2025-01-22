from datetime import date

import sqlalchemy as sa

from crud.base_crud import BaseCrud
from models import SpimexTradingResults


class SpimexTradingCrud(BaseCrud):
    def __init__(self, session):
        super().__init__(session)
        self.model = SpimexTradingResults

    async def get_items_id(self, items_id: int):
        stmt = (
            sa.select(self.model.date)
            .distinct()
            .order_by(self.model.date.desc())
            .limit(items_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_dynamics_params(
        self, date_start: date, date_end: date, data: dict | None = None
    ):
        stmt = sa.select(self.model).filter(
            self.model.date.between(date_start, date_end)
        )
        if data is not None:
            stmt = stmt.filter_by(**data)
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_trading_results_params(self, data: dict | None = None):
        stmt = sa.select(self.model).where(
            self.model.date == (sa.select(sa.func.max(self.model.date))
        ).scalar_subquery())
        if data is not None:
            stmt = stmt.filter_by(**data)
        result = await self.session.scalars(stmt)
        return result.all()
