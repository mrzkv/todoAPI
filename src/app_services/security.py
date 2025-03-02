import hashlib
import re
from src.app_services.config import tokens_config
from src.app_services.database_functions import get_userid
from authx import AuthX, TokenPayload

authx_security = AuthX(config=tokens_config)


async def get_hash(message: str) -> str:
    return hashlib.sha256(message.encode()).hexdigest()


async def check_password_security(password: str) -> bool:
    pattern = r'[A-Za-z0-9@#!$%^&+=]{8,}'
    if re.fullmatch(pattern, password):
        return True
    return False


async def get_token(login: str) -> str:
    return authx_security.create_access_token(uid=str(await get_userid(login)))


async def decode_token(token: str) -> TokenPayload:
    return authx_security._decode_token(token)
