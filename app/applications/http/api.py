from fastapi import FastAPI

from containers.container import Container

from .pages.router import pages_router
from .webrtc.router import web_rtc_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.container = Container()

    # event handler
    app.add_event_handler(
        "shutdown",
        app.container.webrtc_peer_connection_manager().close_all_peer_connections(),
    )

    # routing
    app.include_router(pages_router)
    app.include_router(web_rtc_router)

    return app
