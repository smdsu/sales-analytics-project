import os
from pydantic_settings import BaseSettings, SettingsConfigDict
import redis


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    REDIS_PASSWORD: str
    REDIS_USER: str
    REDIS_USER_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            '..',
            '.env'
        )
    )


settings = Settings()


def get_db_url():
    return (
        f"postgresql+asyncpg://{settings.DB_USER}:"
        f"{settings.DB_PASSWORD}@{settings.DB_HOST}:"
        f"{settings.DB_PORT}/{settings.DB_NAME}"
    )


def get_db_url_without_asyncpg():
    return (
        f"postgresql://{settings.DB_USER}:"
        f"{settings.DB_PASSWORD}@{settings.DB_HOST}:"
        f"{settings.DB_PORT}/{settings.DB_NAME}"
    )


def get_redis_url():
    return (
        f"redis://{settings.REDIS_USER}:"
        f"{settings.REDIS_USER_PASSWORD}@127.0.0.1:6379"
    )


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}


redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    username=settings.REDIS_USER,
    password=settings.REDIS_USER_PASSWORD
)
