from fastapi import APIRouter
from starlette.responses import JSONResponse
from starlette import status
from app_services.schemes import UserSign
from app_services.security import get_hash, check_password_security, get_token
from app_services.database_functions import (check_user_exists,
                              register_user, get_user_password)
from secrets import compare_digest

router = APIRouter(prefix='/v1/api/auth')


@router.post('/sign-up')
async def sign_up(user_data: UserSign) -> JSONResponse:
    if await check_password_security(user_data.password) and len(user_data.login) >= 5:
        if await check_user_exists(login=user_data.login):
            hashed_password = await get_hash(user_data.password)
            await register_user(user_data.login, hashed_password)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    'status':'ok',
                    'message':'account registered'
                }
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    'status':'error',
                    'message':'user already exists'
                }
            )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'status':'error',
                'message':'password un-secure'
            }
        )

@router.post('/sign-in')
async def sign_in(user_data: UserSign):
    password_flag = True
    hashed_password = await get_hash(user_data.password)
    db_hashed_password = await get_user_password(user_data.login)
    if db_hashed_password is None:
        password_flag = False
    if compare_digest(db_hashed_password, hashed_password) and password_flag is True:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'status':'ok',
                'token': await get_token(user_data.login, user_data.password)
            }
        )
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            'status':'error',
            'message':'check your password or email'
        }
    )