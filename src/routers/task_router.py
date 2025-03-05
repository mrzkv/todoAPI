from fastapi import APIRouter, HTTPException, Cookie, status
from src.app_services.database_functions import get_user_task_list, create_user_task, change_user_task_mode
from src.app_services.schemes import CreateTaskScheme, UpdateTaskScheme, TaskMode
from src.app_services.security import decode_token
from src.app_services.config import tokens_config

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
    if creds.mode == TaskMode.ACTIVE or creds.mode == TaskMode.DELETED or creds.mode == TaskMode.COMPLETED:
        new_task = await change_user_task_mode(userid=user_id, taskid=creds.taskid, mode=creds.mode)
        return {'status': 'ok',
                'task': new_task}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={'status': 'error',
                                    'message': 'Incorrect task mode'})
