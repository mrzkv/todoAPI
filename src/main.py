from asyncio import run
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from core.database_core import init_db
from routers.system_router import router as system_router
from routers.sign_router import router as sign_router
from routers.task_router import router as task_router
import uvicorn
from services.config import SERVER_PORT, SERVER_START_TIME, IP_ADDRESS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content={"status": "error",
                                 "message": "Ошибка в данных запроса."})


app.include_router(system_router)
app.include_router(sign_router)
app.include_router(task_router)


def start_server():
    print(f'Server start time - {SERVER_START_TIME}')
    uvicorn.run(
        app='main:app',
        host=IP_ADDRESS,
        port=SERVER_PORT,
        log_level="info",
        reload=True
    )


if __name__ == "__main__":
    run(init_db())
    start_server()
