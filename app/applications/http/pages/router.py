from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request
from starlette.responses import HTMLResponse

from .responses import JavascriptResponse

pages_router = APIRouter()


@pages_router.get("/", response_class=HTMLResponse)
@inject
async def index(
    request: Request,
    templates=Depends(Provide["templates"]),
):
    return templates.TemplateResponse(
        name="index.html",
        context={
            "request": request,
            # add context here.
        },
    )


@pages_router.get("/client.js", response_class=JavascriptResponse)
@inject
async def client_js(
    request: Request,
    templates=Depends(Provide["templates"]),
):
    return templates.TemplateResponse(
        name="client.js",
        context={
            "request": request,
        },
    )
