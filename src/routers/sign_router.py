from secrets import compare_digest

from fastapi import APIRouter, HTTPException, Response, status, Depends
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.database.functions import User
from core.database.helper import db_helper
from core.schemes import SignScheme
from services.security import get_hash, create_token

router = APIRouter(prefix=settings.prefix.AUTH, tags=['auth'])


@router.post('/sign-up')
async def sign_up(creds: SignScheme,
                  session: AsyncSession = Depends(db_helper.get_async_session),
) -> JSONResponse:
    if not await User.check_exists(login=creds.login, session=session):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User with this login already exists')

    await User.register(creds.login, await get_hash(creds.password), session=session)
    logger.info(f"User '{creds.login}' registered")
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            'status': 'ok',
            'message': 'account registered'})


@router.post('/sign-in')
async def sign_in(creds: SignScheme,
                  response: Response,
                  session: AsyncSession = Depends(db_helper.get_async_session)
) -> JSONResponse:
    user_data = await User.get_data_by_login(creds.login, session=session)
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not compare_digest(user_data.hashed_password, await get_hash(creds.password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = await create_token(user_data.id)
    logger.info(f"User '{creds.login}' sign-in successfully")
    response.set_cookie(key=settings.token.JWT_ACCESS_COOKIE_NAME,
                        value=token,
                        httponly=True)
    return {'access_token': token}
