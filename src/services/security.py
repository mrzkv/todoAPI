import hashlib
from core.config import tokens_config
from authx import AuthX

authx_security = AuthX(config=tokens_config)


async def get_hash(message: str) -> str:
    return hashlib.sha256(message.encode()).hexdigest()


async def create_token(user_id: str) -> str:
    return authx_security.create_access_token(uid=str(user_id))


async def decode_token(token: str) -> int | str:
    try:
        token_data = int(authx_security._decode_token(token).sub)
    except:
        token_data = 'Token has expired'
    return token_data
