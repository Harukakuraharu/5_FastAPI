import datetime

from pydantic import BaseModel, ConfigDict


class DateListResponse(BaseModel):
    date: datetime.date


class DynamicsParams(BaseModel):
    oil_id: str | None = None
    delivery_type_id: str | None = None
    delivery_basis_id: str | None = None
    start_date: datetime.date
    end_date: datetime.date


class GetDynamicsResponse(BaseModel):
    id: int
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: str
    total: str
    count: str
    date: datetime.date
    created_on: datetime.datetime
    updated_on: datetime.datetime
    model_config = ConfigDict(from_attributes=True)


class TradingResultsParams(BaseModel):
    oil_id: str | None = None
    delivery_type_id: str | None = None
    delivery_basis_id: str | None = None
