from typing import Annotated

from fastapi import Depends, Query
from fastapi.routing import APIRouter
from services import services

from core import dependency
from schemas import schemas


spimex_routers = APIRouter(prefix="/spimex", tags=["Spimex"])


@spimex_routers.get(
    "/get_last_trading_dates", response_model=list[schemas.DateListResponse]
)
async def get_last_trading_dates(
    session: dependency.AsyncSessionDependency,
    days_count: Annotated[int, Query(ge=1)],
):
    """
    Получение списка дат последних торговых дней
    (фильтрация по кол-ву последних торговых дней)
    """
    return await services.TradeService(session).get_last_trading_dates(
        days_count
    )


@spimex_routers.get(
    "/get_dynamics", response_model=list[schemas.GetDynamicsResponse]
)
async def get_dynamics(
    session: dependency.AsyncSessionDependency,
    params: schemas.DynamicsParams = Depends(),
):
    """
    Получение списка торгов за заданный период
    (фильтрация по oil_id, delivery_type_id, delivery_basis_id, 
    start_date, end_date).
    """
    return await services.TradeService(session).get_dynamics(params)


@spimex_routers.get(
    "/get_trading_results", response_model=list[schemas.GetDynamicsResponse]
)
async def get_trading_results(
    session: dependency.AsyncSessionDependency,
    params: schemas.TradingResultsParams = Depends(),
):
    """
    Получение списка последних торгов
    (фильтрация по oil_id, delivery_type_id, delivery_basis_id)
    """
    return await services.TradeService(session).get_trading_results(params)
