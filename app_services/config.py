import time
import os

server_start_time = time.time()
# server_port = int(os.getenv("SERVER_PORT"))
# ip_address = os.getenv("IP_ADDRESS")
server_port = 8765
ip_address = 'localhost'
DATABASE_URL = 'postgresql+asyncpg://postgres:lolipop@127.0.0.1:5432/bot_users'