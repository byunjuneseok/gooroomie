import asyncio
from asyncio import Queue

import cv2
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from settings import Settings

queue = Queue()
camera = cv2.VideoCapture(0)

templates = Jinja2Templates(directory="templates")

app = FastAPI()
settings = Settings()


class ConnectedClients:

    def __init__(self):
        self.clients = []

    async def add_client(self, client):
        await client.accept()
        self.clients.append(client)
        print(f'Client {client} added, total clients: {len(self.clients)}')

    def remove_client(self, client):
        self.clients.remove(client)

    async def broadcast(self, message=None):
        for client in self.clients:
            try:
                await client.send_bytes(message)
            except Exception:
                self.remove_client(client)


connected_clients = ConnectedClients()


def get_bytes():
    ret, frame = camera.read()
    if not ret:
        return None
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    return frame


async def periodic_broadcast():
    while True:
        if connected_clients.clients:
            await connected_clients.broadcast(message=get_bytes())
        await asyncio.sleep(1/24)


@app.on_event("startup")
async def schedule_periodic():
    loop = asyncio.get_event_loop()
    loop.create_task(periodic_broadcast())


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    websocket_endpoint = f'ws://{settings.base_url}/ws'
    return templates.TemplateResponse("index.html", {'request': request, 'websocket_endpoint': websocket_endpoint})


@app.websocket('/ws')
async def broadcast(websocket: WebSocket):
    await connected_clients.add_client(websocket)
    while True:
        await asyncio.sleep(1/24)
