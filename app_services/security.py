import hashlib
import re
import jwt
import subprocess


async def get_hash(message: str) -> str:
    return hashlib.sha256(message.encode()).hexdigest()

async def check_password_security(password: str) -> bool:
    pattern = r'[A-Za-z0-9@#!$%^&+=]{8,}'
    if re.fullmatch(pattern, password):
        return True
    return False

async def get_token(login: str, password: str):

    return 'asfglahlrl3wtgs.gshjkldjh3'
