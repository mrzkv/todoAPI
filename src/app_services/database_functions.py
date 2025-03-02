from src.app_core.database_core import get_async_session
from src.app_services.database_tables import UserData
from sqlalchemy.future import select


async def check_user_exists(login: str) -> bool:
    async for session in get_async_session():
        result = await session.execute(
            select(UserData.id)
            .where(UserData.login == login))
        if result.scalar():
            return False
        return True


async def register_user(login: str, hashed_password: str) -> None:
    async for session in get_async_session():
        reg_data = [UserData(
            login=login,
            hashed_password=hashed_password)]
        session.add_all(reg_data)
        await session.commit()


async def get_user_password(login: str) -> str | None:
    async for session in get_async_session():
        result = await session.execute(
            select(UserData.hashed_password)
            .where(UserData.login == login))
        if result:
            return result.scalar()


async def get_userid(login: str) -> int | None:
    async for session in get_async_session():
        result = await session.execute(
            select(UserData.id)
            .where(UserData.login == login))
        if result:
            return int(result.scalar())

