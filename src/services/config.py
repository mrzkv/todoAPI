import time
from authx import AuthXConfig
from datetime import timedelta

SERVER_START_TIME = int(time.time())
SERVER_PORT = 8765
IP_ADDRESS = 'localhost'
DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/bot_users'

tokens_config = AuthXConfig()
tokens_config.JWT_SECRET_KEY = 'SECRET_KEY'
tokens_config.JWT_TOKEN_LOCATION = ['cookies']
tokens_config.JWT_ACCESS_COOKIE_NAME = 'my_access_token'
tokens_config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=600)
