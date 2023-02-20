from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

from core.config import settings
from core.templates import templates

router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    websocket_endpoint = f'ws://{settings.base_url}/ws'
    return templates.TemplateResponse(
        "index.html",
        {'request': request, 'websocket_endpoint': websocket_endpoint}
    )
