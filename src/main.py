from asyncio import run
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from routers.system_router import router as system_router
from routers.sign_router import router as sign_router
from routers.task_router import router as task_router
import uvicorn
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from core.database.helper import db_helper
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

app.include_router(system_router)
app.include_router(sign_router)
app.include_router(task_router)


def start_server():
    print(f'Server start time - {int(settings.SERVER_START_TIME)}')
    uvicorn.run(
        app='main:app',
        host=settings.IP_ADDRESS,
        port=settings.SERVER_PORT,
        log_level="info",
        reload=True
    )


if __name__ == "__main__":
    run(db_helper.init_db())
    start_server()