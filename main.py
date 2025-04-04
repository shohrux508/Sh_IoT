import asyncio
import time

from fastapi import FastAPI, WebSocket

from IoT.mqtt_manager import ManageBroker
from database.requests import Devices, Clients
from routers.example import router

app = FastAPI()

app.include_router(router=router)
active_connections = []

@app.get('/')
async def welcome():
    return {"message": 'Hello, world!!!'}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    while True:
        data = await websocket.receive_text()
        data = data.lower()
        await websocket.send_text(f"Получено: {data}!")
        time.sleep(2)
        await websocket.send_text(f'{data}')
        time.sleep(1)

async def broadcast_message(message: str):
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")

# Пример фоновой задачи, имитирующей получение сообщений от брокера
async def broker_listener():
    while True:
        message = ManageBroker().subscribe('devices/1/control')
        await asyncio.sleep(5)
        print(f"MESSAGE: {message}")
        await broadcast_message(message)