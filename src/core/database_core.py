from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from services.database_tables import *
from services.config import DATABASE_URL

# Configure async engine and session
engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


# Get AsyncSession for work with DataBase
async def get_async_session():
    """
    async for session in get_async_session():
    """
    async with AsyncSessionFactory() as session:
        yield session


# Init tables in DataBase
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
