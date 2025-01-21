from contextlib import asynccontextmanager, contextmanager
from typing import AsyncIterator, Iterator
from urllib.parse import urlsplit, urlunsplit

import sqlalchemy as sa
from alembic.config import Config
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import create_async_engine

from core.settings import config as project_config



# Функция для создания нового alembic config  для тестов, т.к. в файле env.py у alembic 
# подвязан под основую БД, которая будет использоваться в проекте.
# project_config.ROOT_DIR - формируем путь до alembic.ini,
# далее подменяем is_testing на True (по дефолту False), а базовый
# URL sqlalchemy.url до сгенерированного нового (в фикстурах), в конце
# указываем папку для миграций в script_location,т.к. alembic сам не видит путь
def make_alembic_config(
    dsn: str, script_location: str | None = None
) -> Config:
    """
    Create alembic.config for tests for create test database.

    :param dsn: main URL for test database on postgres_fixture.
    :param script_location: name path for alembic

    :return: alembic config for test database.
    """
    alembic_cfg = Config(f"{project_config.ROOT_DIR}/alembic.ini")
    alembic_cfg.set_main_option("is_testing", "True")
    alembic_cfg.set_main_option("sqlalchemy.url", dsn)
    if script_location:
        alembic_cfg.set_main_option(
            "script_location", f"{script_location}:migrations"
        )

    return alembic_cfg



# Создание БД с URL, сформированным в tmp_database.
# make_url формирует URL для подключения, который будет принимает SQLAlchemy
# URL с "postgres" уже существует по дефолту, т.е. ее создавать не нужно,
# можно подкючаться сразу через create_engine
# и создать движок на основе postgres и тестовую БД с тестовым именем.
def create_database(
    url: str,
    template: str = "template1",
    encoding: str = "utf8",
) -> None:
    """
    Create database with test url.

    :param url: main URL for test database on postgres_fixture.
    :param template: name template for in test database.
    :param encodind: encoding for create test database

    """
    url_obj = make_url(url)
    main_url = url_obj._replace(database="postgres")
    engine = sa.create_engine(main_url, isolation_level="AUTOCOMMIT")
    with engine.begin() as conn:
        text = (
            f"CREATE DATABASE {url_obj.database} ENCODING '{encoding}'"
            f"TEMPLATE {template};"
        )

        conn.execute(sa.text(text))
    engine.dispose()


def drop_database(url: str) -> None:
    """
    Delete test database

    :param url: main URL for test database on postgres_fixture.

    """
    url_obj = make_url(url)
    main_url = url_obj._replace(database="postgres")
    engine = sa.create_engine(main_url, isolation_level="AUTOCOMMIT")
    with engine.begin() as conn:
        text = f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{url_obj.database}'
            AND pid <> pg_backend_pid();
            """
        conn.execute(sa.text(text))
        text = f"DROP DATABASE {url_obj.database}"
        conn.execute(sa.text(text))
    engine.dispose()


async def async_create_database(
    url: str,
    template: str = "template1",
    encoding: str = "utf8",
) -> None:
    """
    Async create database with test url

    :param url: main URL for test database on postgres_fixture.
    :param template: name template for in test database.
    :param encodind: encoding for create test database

    """
    url_obj = make_url(url)
    main_url = url_obj._replace(database="postgres")
    engine = create_async_engine(main_url, isolation_level="AUTOCOMMIT")
    async with engine.begin() as conn:
        text = (
            f"CREATE DATABASE {url_obj.database} ENCODING '{encoding}'"
            f"TEMPLATE {template};"
        )

        await conn.execute(sa.text(text))
    await engine.dispose()


async def async_drop_database(url: str) -> None:
    """
    Async delete test database

    :param url: main URL for test database on postgres_fixture.

    """
    url_obj = make_url(url)
    main_url = url_obj._replace(database="postgres")
    engine = create_async_engine(main_url, isolation_level="AUTOCOMMIT")
    async with engine.begin() as conn:
        text = f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{url_obj.database}'
            AND pid <> pg_backend_pid();
            """
        await conn.execute(sa.text(text))
        text = f"DROP DATABASE {url_obj.database}"
        await conn.execute(sa.text(text))
    await engine.dispose()



# Формирование URL для тестовой БД для миграций, 
# на вход передается URL для подключения от фикстур
@contextmanager
def tmp_database(str_url: str, db_name: str = "", **kwargs) -> Iterator[str]:
    """
    Create URL for test database

    :param str_url: URL with localhost on fixture.
    :param db_name: name for test database.

    """
    tmp_db_url = urlsplit(str_url)
    str_url = urlunsplit(tmp_db_url._replace(path=f"/{db_name}"))
    create_database(str_url, **kwargs)

    try:
        yield str_url
    finally:
        drop_database(str_url)


@asynccontextmanager
async def async_tmp_database(
    str_url: str, db_name: str = "", **kwargs
) -> AsyncIterator[str]:
    """
    Async create URL for test database

    :param str_url: URL with localhost on fixture.
    :param db_name: name for test database.    
    
    """
    tmp_db_url = urlsplit(str_url)
    str_url = urlunsplit(tmp_db_url._replace(path=f"/{db_name}"))
    try:
        await async_create_database(str_url, **kwargs)
    except ProgrammingError:
        await async_drop_database(str_url)
        await async_create_database(str_url, **kwargs)
    try:
        yield str_url
    finally:
        await async_drop_database(str_url)
