from pydantic import computed_field
from pydantic_settings import BaseSettings


class Config(BaseSettings):

    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "user"
    POSTGRES_DB: str = "db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    REDIS_HOST: str = "localhost"

    TIMEZONE: str = 'Asia/Yekaterinburg'

    @computed_field
    def async_dsn(self) -> str:
        """URL for DB"""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.POSTGRES_DB}"
        )

    @computed_field
    def dsn(self) -> str:
        """URL for alembic"""
        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.POSTGRES_DB}"
        )

    @computed_field
    def redis_url(self) -> str:
        """URL for Redis"""
        return f"redis://{self.REDIS_HOST}:6379/1"

    @computed_field
    def celery_url(self) -> str:
        """URL for Celery"""
        return f"redis://{self.REDIS_HOST}:6379/2"


config = Config()
