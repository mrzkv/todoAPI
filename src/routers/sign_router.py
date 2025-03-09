from secrets import compare_digest

from fastapi import APIRouter, HTTPException, Response
from services.config import tokens_config
from services.database_functions import (check_user_exists,
                                         register_user, get_user_password)
from services.schemes import SignScheme
from services.security import get_hash, get_token
from starlette import status
from starlette.responses import JSONResponse

router = APIRouter(prefix='/v1/api/auth')


@router.post('/sign-up')
async def sign_up(creds: SignScheme) -> JSONResponse:
    if await check_user_exists(login=creds.login):
        await register_user(creds.login, await get_hash(creds.password))
        return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    'status': 'ok',
                    'message': 'account registered'
                }
            )
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User with this login already exists')


@router.post('/sign-in')
async def sign_in(creds: SignScheme, response: Response):
    if compare_digest(await get_user_password(creds.login), await get_hash(creds.password)):
        token = await get_token(creds.login)
        response.set_cookie(tokens_config.JWT_ACCESS_COOKIE_NAME, token)
        return {'access_token': token}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
