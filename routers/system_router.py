import time
from fastapi import APIRouter
import asyncio
from starlette import status
from starlette.responses import JSONResponse

from app_services.config import server_start_time, ip_address, server_port

router = APIRouter()

@router.get('/v1/api/ping')
async def ping_handler() -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={ 'ok':'True',
                                  'uptime':f'{time.time()-server_start_time}' })

@router.get('/')
async def bad_url_handler() -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                        content={ 'status':'error',
                                  'detail':f'go to {ip_address}:{server_port}/v1/api'})