from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app_services.config import DATABASE_URL
from app_services.database_tables import *

# Настройка асинхронного движка и сессии
engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_async_session():
    """
    async for session in get_async_session():
    """
    async with AsyncSessionFactory() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

