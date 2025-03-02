import asyncio

from fastapi import FastAPI
from src.app_core.database_core import init_db
from src.routers.system_router import router as system_router
from src.routers.sign_router import router as sign_router
import uvicorn
from src.app_services.config import server_start_time, ip_address, server_port


app = FastAPI()
app.include_router(system_router)
app.include_router(sign_router)


def start_server():
    print(f'Server start time - {server_start_time}')
    uvicorn.run(
        app='main:app',
        host=ip_address,
        port=server_port,
        log_level="info",
        reload=True
    )


if __name__ == "__main__":
    asyncio.run(init_db())
    start_server()