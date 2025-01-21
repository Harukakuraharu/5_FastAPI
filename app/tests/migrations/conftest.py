from typing import Iterator

import pytest
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from core.settings import config
from tests.utils import make_alembic_config, tmp_database


@pytest.fixture(scope="package", name="pg_url")
def pg_url_fixture() -> str:
    """
    Create URL for test database with localhost.
    :return: URL with database.
    """
    config.DB_HOST = "localhost"
    return config.dsn


@pytest.fixture(name="postgres")
def postgres_fixture(pg_url: str) -> Iterator[str]:
    """
    Create main URL for test database.

    :param pg_url: URL with localhost on previous fixture.
    :return: main URL for test database.

    """
    with tmp_database(pg_url, db_name="test_db") as tmp_url:
        yield tmp_url


@pytest.fixture(name="postgres_engine")
def postgres_engine_fixture(
    postgres: str,
) -> Iterator[Engine]:
    """
    Create engine for test database.

    :param postgres: main URL for test database on previous fixture.
    :return: engine for connect with test database.
    """
    engine = create_engine(postgres, echo=False)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture(name="alembic_config")
def alembic_config_fixture(postgres: str) -> Config:
    """
    Update alembic config for test database.

    :param postgres: main URL for test database on postgres_fixture.
    :return: alembic config for test database.
    """
    return make_alembic_config(postgres, "app")
