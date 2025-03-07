from fastapi import APIRouter, HTTPException, Response
from starlette.responses import JSONResponse
from starlette import status
from services.config import tokens_config
from services.schemes import SignScheme
from services.security import get_hash, check_password_security, get_token
from services.database_functions import (check_user_exists,
                                             register_user, get_user_password)
from secrets import compare_digest

router = APIRouter(prefix='/v1/api/auth')


@router.post('/sign-up')
async def sign_up(creds: SignScheme) -> JSONResponse:
    if await check_password_security(creds.password) and len(creds.login) >= 5:
        if await check_user_exists(login=creds.login):
            await register_user(creds.login, await get_hash(creds.password))
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    'status': 'ok',
                    'message': 'account registered'
                }
            )
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/sign-in')
async def sign_in(creds: SignScheme, response: Response):
    if compare_digest(await get_user_password(creds.login), await get_hash(creds.password)):
        token = await get_token(creds.login)
        response.set_cookie(tokens_config.JWT_ACCESS_COOKIE_NAME, token)
        return {'access_token': token}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
