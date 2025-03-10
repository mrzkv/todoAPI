from fastapi import APIRouter, HTTPException, Cookie, status, Depends
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.database.functions import Task
from core.database.helper import db_helper
from core.schemes import CreateTaskScheme, UpdateTaskScheme
from services.security import decode_token

router = APIRouter(prefix=settings.prefix.TASK, tags=['tasks'])


@router.get(path='/list')
async def user_task_list(token: str = Cookie(alias=settings.token.JWT_ACCESS_COOKIE_NAME),
                         session: AsyncSession = Depends(db_helper.get_async_session)
) -> JSONResponse:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    user_id = await decode_token(token)
    if not user_id or user_id == 'Token has expired':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    logger.info(f"User '{user_id}' view his tasks")
    tasks = await Task.get_list(user_id, session=session)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'tasks': tasks}
    )


@router.post(path='/create')
async def user_create_new_task(creds: CreateTaskScheme,
                               token: str = Cookie(alias=settings.token.JWT_ACCESS_COOKIE_NAME),
                               session: AsyncSession = Depends(db_helper.get_async_session)
) -> JSONResponse:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is missing')
    user_id = await decode_token(token)
    if not user_id or user_id == 'Token has expired':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    logger.info(f"User '{user_id}' create new task '{creds.name}'")
    await Task.create(userid=user_id, taskname=creds.name, session=session)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={
                            'status': 'ok',
                            'message': f"task '{creds.name}' has created"
                        }
    )


@router.patch(path='/change-mode')
async def user_change_task_mode(creds: UpdateTaskScheme,
                                token: str = Cookie(alias=settings.token.JWT_ACCESS_COOKIE_NAME),
                                session: AsyncSession = Depends(db_helper.get_async_session)
) -> JSONResponse:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is missing')
    user_id = await decode_token(token)
    if not user_id or user_id == 'Token has expired':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

    await Task.change_mode(userid=user_id, taskid=creds.taskid,
                           mode=creds.mode, session=session)
    logger.info(f"User '{user_id}' change task mode '{creds.mode}'"
                f" in task '{creds.taskid}'")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'status': 'ok',
            'message': f"task '{creds.taskid}' has changed mode"
        }
    )
