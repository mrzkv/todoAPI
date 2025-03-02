import time
import os
from authx import AuthXConfig

server_start_time = time.time()
# server_port = int(os.getenv("SERVER_PORT"))
# ip_address = os.getenv("IP_ADDRESS")
server_port = 8765
ip_address = 'localhost'
DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/bot_users'

tokens_config = AuthXConfig()
tokens_config.JWT_SECRET_KEY = 'SECRET_KEY'
tokens_config.JWT_TOKEN_LOCATION = ['cookies']
tokens_config.JWT_ACCESS_COOKIE_NAME = 'my_access_token'



