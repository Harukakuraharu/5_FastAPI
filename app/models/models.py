import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class SpimexTradingResults(Base):
    __tablename__ = "spimex_trading_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str]
    exchange_product_name: Mapped[str]
    oil_id: Mapped[str]
    delivery_basis_id: Mapped[str]
    delivery_basis_name: Mapped[str]
    delivery_type_id: Mapped[str]
    volume: Mapped[str]
    total: Mapped[str]
    count: Mapped[str]
    date: Mapped[str]
    created_on: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()  # pylint: disable=E1102
    )
    updated_on: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()  # pylint: disable=E1102
    )
