import time
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from core.config import settings

router = APIRouter()


@router.get('/v1/api/ping')
async def ping_handler() -> JSONResponse:
    return {'uptime': int(time.time()-settings.SERVER_START_TIME)}


@router.get('/')
async def bad_url_handler() -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                        content={'status': 'error',
                                 'detail': f'go to {settings.IP_ADDRESS}:{settings.SERVER_PORT}/v1/api'})
