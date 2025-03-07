from sqlalchemy import update
from core.database_core import get_async_session
from services.database_tables import UserData, TaskList, TaskMode
from sqlalchemy.future import select
from typing import List


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


async def get_user_data_by_userid(userid: int) -> UserData | None:
    async for session in get_async_session():
        result = await session.execute(
            select(UserData)
            .where(UserData.id == userid))
        if result:
            return result.scalar()


async def get_user_task_list(userid: int) -> List[dict]:
    async for session in get_async_session():
        result = await session.execute(
            select(TaskList.id, TaskList.name, TaskList.mode)
            .order_by(TaskList.id.asc())
            .where(TaskList.user_id == int(userid)))
        if result:
            return [{"id": row["id"], "name": row["name"], "mode": row["mode"]} for row in result.mappings().all()]


async def create_user_task(userid: int, taskname: str) -> None:
    async for session in get_async_session():
        task_data = [TaskList(
            user_id=userid,
            name=taskname,
            mode=TaskMode.ACTIVE)]
        session.add_all(task_data)
        await session.commit()


async def change_user_task_mode(userid: int, taskid: int, mode: str) -> dict | None:
    async for session in get_async_session():
        stmt = (
            update(TaskList)
            .where(TaskList.user_id == userid, TaskList.id == taskid)
            .values(mode=mode)
            .returning(TaskList.id, TaskList.name, TaskList.mode)
        )
        result = await session.execute(stmt)
        updated_task = result.mappings().first()

        await session.commit()
        return dict(updated_task) if updated_task else None
