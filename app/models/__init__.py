from typing import Type, TypeVar

from models.base import Base
from models.models import SpimexTradingResults

MODEL = TypeVar("MODEL", bound=Base)

TypeModel = Type[MODEL]
