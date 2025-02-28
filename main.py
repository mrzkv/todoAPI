import asyncio

from fastapi import FastAPI

from app_core.database_core import init_db
from routers.system_router import router as system_router
from routers.sign_router import router as sign_router
import uvicorn
from app_services.config import server_start_time, ip_address, server_port

app = FastAPI()
app.include_router(system_router)
app.include_router(sign_router)

def start_server():
    print(f'Server start time - {server_start_time}')
    uvicorn.run(
        'main:app',
        host=ip_address,
        port=server_port,
        log_level="info",
        reload=True
    )

if __name__ == "__main__":
    start_server()
