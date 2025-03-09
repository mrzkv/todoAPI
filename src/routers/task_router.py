from fastapi import APIRouter, HTTPException, Cookie, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from core.database.functions import User, Task
from core.database.helper import db_helper
from core.schemes import CreateTaskScheme, UpdateTaskScheme
from services.security import decode_token
from core.config import tokens_config
from typing import Annotated

router = APIRouter(prefix='/v1/api/tasks')


@router.get(path='/list')
async def user_task_list(token: str = Cookie(alias=tokens_config.JWT_ACCESS_COOKIE_NAME),
                         session: AsyncSession = Depends(db_helper.get_async_session)
) -> JSONResponse:

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    user_id = await decode_token(token)
    if not user_id or user_id == 'Token has expired':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    tasks = await Task.get_list(user_id, session=session)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'tasks': tasks}
    )


@router.post(path='/create')
async def user_create_new_task(creds: CreateTaskScheme,
                               token: str = Cookie(alias=tokens_config.JWT_ACCESS_COOKIE_NAME),
                               session: AsyncSession = Depends(db_helper.get_async_session)
) -> JSONResponse:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is missing')
    user_id = await decode_token(token)
    if not user_id or user_id == 'Token has expired':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

    await Task.create(userid=user_id, taskname=creds.name, session=session)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={
                            'status': 'ok',
                            'message': f"task '{creds.name}' has created"
                        }
    )


@router.patch(path='/change-mode')
async def user_change_task_mode(creds: UpdateTaskScheme,
                                token: str = Cookie(alias=tokens_config.JWT_ACCESS_COOKIE_NAME),
                                session: AsyncSession = Depends(db_helper.get_async_session)
) -> JSONResponse:
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is missing')
    user_id = await decode_token(token)
    if not user_id or user_id == 'Token has expired':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

    await Task.change_mode(userid=user_id, taskid=creds.taskid,
                           mode=creds.mode, session=session)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'status': 'ok',
            'message': f"task '{creds.taskid}' has changed mode"
        }
    )
