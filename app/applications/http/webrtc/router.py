from typing import TYPE_CHECKING

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from .schemas import Description

if TYPE_CHECKING:
    from handlers.webrtc.peer_connection_manager import WebRTCPeerConnectionManager

web_rtc_router = APIRouter(prefix="/webrtc/v1")


@web_rtc_router.post("/offers")
@inject
async def offers(
    body: Description,
    webrtc_peer_connection_manager: "WebRTCPeerConnectionManager" = Depends(Provide["webrtc_peer_connection_manager"]),
):
    answer = await webrtc_peer_connection_manager.create_answer(
        offer=body.to_rtc_session_description(),
    )
    return Description.from_rtc_session_description(answer)
