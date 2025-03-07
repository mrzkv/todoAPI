import time
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from services.config import SERVER_START_TIME, SERVER_PORT, IP_ADDRESS

router = APIRouter()


@router.get('/v1/api/ping')
async def ping_handler() -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={'uptime': f'{int(time.time()) - SERVER_START_TIME}'})


@router.get('/')
async def bad_url_handler() -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                        content={'status': 'error',
                                 'detail': f'go to {IP_ADDRESS}:{SERVER_PORT}/v1/api'})
