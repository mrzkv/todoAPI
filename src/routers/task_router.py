from fastapi import APIRouter, HTTPException, Cookie, status
from services.database_functions import get_user_task_list, create_user_task, change_user_task_mode
from services.schemes import CreateTaskScheme, UpdateTaskScheme, TaskMode
from services.security import decode_token
from services.config import tokens_config

router = APIRouter(prefix='/v1/api/tasks')


@router.get(path='/list')
async def user_task_list(token: str = Cookie(alias=tokens_config.JWT_ACCESS_COOKIE_NAME)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    user_id = await decode_token(token)
    if not user_id or user_id == 'Token has expired':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    tasks = await get_user_task_list(user_id)
    return {'tasks': tasks}


@router.post(path='/create')
async def user_create_new_task(creds: CreateTaskScheme,
                               token: str = Cookie(alias=tokens_config.JWT_ACCESS_COOKIE_NAME)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is missing')
    user_id = await decode_token(token)

    if not user_id or user_id == 'Token has expired':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    await create_user_task(userid=user_id, taskname=creds.name)
    return {'status': 'ok',
            'message': f"task '{creds.name}' has created"}


@router.patch(path='/change-mode')
async def user_change_task_mode(creds: UpdateTaskScheme,
                                token: str = Cookie(alias=tokens_config.JWT_ACCESS_COOKIE_NAME)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is missing')
    user_id = await decode_token(token)
    if not user_id or user_id == 'Token has expired':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    new_task = await change_user_task_mode(userid=user_id, taskid=creds.taskid, mode=creds.mode)
    return {'status': 'ok',
            'task': new_task}
