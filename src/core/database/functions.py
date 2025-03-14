from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.helper import db_helper
from core.database.tables import UserData, TaskList, TaskMode
from sqlalchemy.future import select
from typing import List
from loguru import logger


class User:
    @staticmethod
    @logger.catch
    async def check_exists(login: str,
                           session: AsyncSession) -> bool:
        result = await session.execute(
            select(UserData.id)
            .where(UserData.login == login))
        if result.scalar():
            logger.info(f"User '{login}' check exists")
            return False
        return True

    @staticmethod
    @logger.catch
    async def register(login: str,
                       hashed_password: str,
                       session: AsyncSession) -> None:
        logger.info(f"User '{login}' added to db")
        reg_data = [UserData(
            login=login,
            hashed_password=hashed_password)]
        session.add_all(reg_data)
        await session.commit()

    @staticmethod
    @logger.catch
    async def get_data_by_id(user_id: str,
                             session: AsyncSession) -> UserData:
        result = await session.execute(
            select(UserData)
            .where(UserData.id == user_id))
        return result.scalar()

    @staticmethod
    @logger.catch
    async def get_data_by_login(login: str,
                                session: AsyncSession) -> UserData:
        result = await session.execute(
            select(UserData)
            .where(UserData.login == login))
        return result.scalar()


class Task:
    @staticmethod
    @logger.catch
    async def get_list(userid: int,
                       session: AsyncSession) -> List[dict]:
        result = await session.execute(
            select(TaskList.id, TaskList.name, TaskList.mode)
            .order_by(TaskList.id.asc())
            .where(TaskList.user_id == int(userid)))
        return [{"id": row["id"], "name": row["name"], "mode": row["mode"]}
                for row in result.mappings().all()]

    @staticmethod
    @logger.catch
    async def create(userid: int, taskname: str,
                     session: AsyncSession) -> None:
        logger.info(f"User '{userid}' task '{taskname}' added to db")
        task_data = [TaskList(
            user_id=userid,
            name=taskname,
            mode=TaskMode.ACTIVE)]
        session.add_all(task_data)
        await session.commit()

    @staticmethod
    @logger.catch
    async def change_mode(userid: int, taskid: int,
                          mode: str, session: AsyncSession) -> None:
        await session.execute(
            update(TaskList)
            .where(TaskList.user_id == userid, TaskList.id == taskid)
            .values(mode=mode))
        logger.info(f"User {userid} changed task mode '{mode}' on '{taskid}'")
        await session.commit()
