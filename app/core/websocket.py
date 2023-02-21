from typing import List

from fastapi import WebSocket


class ConnectedClients:

    def __init__(self):
        self.clients: List[WebSocket] = []

    async def add_client(self, client: WebSocket) -> None:
        await client.accept()
        self.clients.append(client)
        print(f'Client {client} added, total clients: {len(self.clients)}')

    def remove_client(self, client: WebSocket) -> None:
        self.clients.remove(client)

    async def broadcast(self, message=None) -> None:
        for client in self.clients:
            try:
                await client.send_bytes(message)
            except Exception:
                self.remove_client(client)


connected_clients = ConnectedClients()
