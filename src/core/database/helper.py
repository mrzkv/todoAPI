from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (create_async_engine, AsyncEngine,
                                    async_sessionmaker, AsyncSession)
from core.config import settings
from core.database.tables import Base
from loguru import logger


class DatabaseHelper:
    def __init__(
            self,
            url: str,
            echo: bool = False,
            echo_pool: bool = False,
            pool_size: int = 5,
            max_overflow: int = 10, ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow, )

        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False, )

    @logger.catch
    async def dispose(self) -> None:
        logger.info('engine disposed')
        await self.engine.dispose()

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            logger.info(f'session created.')
            yield session

    @logger.catch
    async def init_db(self):
        async with self.engine.begin() as conn:
            logger.info(f'tables created.')
            await conn.run_sync(Base.metadata.create_all)


db_helper = DatabaseHelper(
    url=settings.db.DATABASE_URL,
    echo=False,
    echo_pool=False,
    pool_size=settings.db.POOL_SIZE,
    max_overflow=settings.db.MAX_OVERFLOW,
)
