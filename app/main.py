import asyncio

import cv2
from fastapi import FastAPI, WebSocket

from api.api import api_router
from core.camera import camera
from core.config import settings
from core.websocket import connected_clients

app = FastAPI()
app.include_router(api_router)


def get_bytes():
    ret, frame = camera.read()
    if not ret:
        return None
    ret, buffer = cv2.imencode('.webp', frame, [cv2.IMWRITE_WEBP_QUALITY, 100])
    frame = buffer.tobytes()
    return frame


async def periodic_broadcast():
    while True:
        if connected_clients.clients:
            await connected_clients.broadcast(message=get_bytes())
        await asyncio.sleep(1/settings.frame_rate)


@app.on_event("startup")
async def schedule_periodic():
    loop = asyncio.get_event_loop()
    loop.create_task(periodic_broadcast())


@app.websocket('/ws')
async def broadcast(websocket: WebSocket):
    await connected_clients.add_client(websocket)
    while True:
        await asyncio.sleep(settings.health_check_interval)
