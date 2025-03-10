import hashlib
from authx import AuthX
from loguru import logger
from core.config import settings

authx_security = AuthX(config=settings.token)


@logger.catch
async def get_hash(message: str) -> str:
    return hashlib.sha256(message.encode()).hexdigest()


@logger.catch
async def create_token(user_id: str) -> str:
    token = authx_security.create_access_token(uid=str(user_id))
    logger.info(f'Token created for {user_id}')
    return token


@logger.catch
async def decode_token(token: str) -> int | str:
    try:
        token_data = int(authx_security._decode_token(token).sub)
    except:
        token_data = 'Token has expired'
    logger.info(f'Token decoded: {token_data}')
    return token_data
