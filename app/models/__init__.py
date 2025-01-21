from typing import Type, TypeVar

from models.base import Base


MODEL = TypeVar("MODEL", bound=Base)

TypeModel = Type[MODEL]
