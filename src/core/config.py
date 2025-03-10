from datetime import datetime, timedelta
import time
from authx import AuthXConfig
from pydantic_settings import BaseSettings
from loguru import logger


class DatabaseSettings(BaseSettings):
    DATABASE_URL: str
    POOL_SIZE: int = 50
    MAX_OVERFLOW: int = 10


class RoutersPrefix(BaseSettings):
    TASK: str
    AUTH: str


class LoggerSettings(BaseSettings):
    filename: str = "app"
    extension: str = ".log"
    level: str = "DEBUG"
    rotation: str = "12:00"
    serialize: bool = False
    compression: str = "zip"
    format: str = "{time} {level} {message}"


class Settings(BaseSettings):
    SERVER_START_TIME: int
    SERVER_PORT: int = 8765
    IP_ADDRESS: str = 'localhost'
    db: DatabaseSettings
    prefix: RoutersPrefix
    token: AuthXConfig
    logger: LoggerSettings


settings = Settings(
    SERVER_START_TIME=int(time.time()),
    SERVER_PORT=8765,
    IP_ADDRESS='127.0.0.1',
    db=DatabaseSettings(
        DATABASE_URL='postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/bot_users',
        POOL_SIZE=50,
        MAX_OVERFLOW=10
    ),
    prefix=RoutersPrefix(
        TASK='/v1/api/tasks',
        AUTH='/v1/api/auth'
    ),
    token=AuthXConfig(
        JWT_SECRET_KEY='SECRET_KEY',
        JWT_TOKEN_LOCATION=['cookies'],
        JWT_ACCESS_COOKIE_NAME='my_access_token',
        JWT_ACCESS_TOKEN_EXPIRES=int(timedelta(minutes=600).total_seconds())
    ),
    logger=LoggerSettings(
        filename="app",
        extension=".log",
        level="DEBUG",
        compression="zip",
        rotation="5MB",
        serialize=False,
        format="{time} {level} {message}"
    )
)

logger.add(
    sink=f'{settings.logger.filename}{settings.logger.extension}',
    level=settings.logger.level,
    format=settings.logger.format,
    serialize=settings.logger.serialize,
    rotation=settings.logger.rotation,
    compression=settings.logger.compression,
)
