from fastapi.routing import APIRouter
from api import pages


api_router = APIRouter()
api_router.include_router(pages.router, prefix="", tags=["pages"])
