import sqlalchemy as sa
from fastapi import Depends
from fastapi.routing import APIRouter

from core import dependency
from core.dependency import AsyncSessionDependency
from models import SpimexTradingResults
from schemas import schemas
from crud.spimex_trading import SpimexTradingCrud
from typing import Annotated

from fastapi import FastAPI, Query



spimex_routers = APIRouter(prefix="/spimex", tags=["Spimex"])


@spimex_routers.get("/get_last_trading_dates", response_model=list[schemas.DateListResponse])
async def get_last_trading_dates(
    session: dependency.AsyncSessionDependency, days_count: Annotated[int, Query(ge=1)]
):
    """
    Получение списка дат последних торговых дней (фильтрация по кол-ву последних торговых дней)
    """
    days = await SpimexTradingCrud(session).get_items_id(days_count)
    return days



@spimex_routers.get("/get_dynamics", response_model=list[schemas.GetDynamicsResponse])
async def get_dynamics(session: dependency.AsyncSessionDependency, 
                       params: schemas.DynamicsParams = Depends()):
    """
    Получение списка торгов за заданный период 
    (фильтрация по oil_id, delivery_type_id, delivery_basis_id, start_date, end_date).
    """
    data = params.model_dump(exclude_unset=True)
    data = {key: value for key, value in data.items() if value is not None}
    start_date = data.pop("start_date")
    end_date = data.pop("end_date")
    response = await SpimexTradingCrud(session).get_dynamics_params(start_date, end_date, data or None)
    return response

# @spimex_routers.get("/", response_model=...)
# async def get_trading_results(session: dependency.AsyncSessionDependency):
#     """
#     Получение списка торгов (фильтрация по oil_id, delivery_type_id, delivery_basis_id)
#     """
#     pass
