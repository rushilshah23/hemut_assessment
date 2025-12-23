from typing import Set
from fastapi import WebSocket
from src.helpers.enums.user import RoleEnum



class ConnectionManager:
    def __init__(self):
        self.active_connections: list[tuple[WebSocket, dict]] = []

    async def connect(self, websocket: WebSocket, user: dict):
        await websocket.accept()
        self.active_connections.append((websocket, user))

    def disconnect(self, websocket: WebSocket):
        self.active_connections = [
            (ws, u) for ws, u in self.active_connections if ws != websocket
        ]

    async def broadcast(self, message: dict):
        for ws, _ in self.active_connections:
            await ws.send_json(message)

    async def broadcast_to_admins(self, message: dict):
        for ws, user in self.active_connections:
            if user and user.get("role") == RoleEnum.ADMIN.value:
                await ws.send_json(message)
