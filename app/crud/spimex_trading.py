from typing import Any, Sequence

import sqlalchemy as sa

from crud.base_crud import BaseCrud
from models import SpimexTradingResults
from datetime import date

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
        return result.all()


    # async def get_filter_date(self, fields, param):
    #     stmt = sa.select(self.model).where(self.model.fields == param)
    #     result = await self.session.execute(stmt)
    #     return result.all()

    async def get_dynamics_params(self, date_start: date, date_end: date, data: dict | None = None):

        stmt = sa.select(self.model).filter(self.model.date.between(date_start, date_end))
        if data is not None:
            stmt = stmt.filter_by(**data)
        result = await self.session.scalars(stmt)
        return result.all()
