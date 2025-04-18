import asyncio
import time

from fastapi import FastAPI, WebSocket
from database.engine import init_db
from database.requests import Devices, Users
from routers.devices_rt import router as rt1
from routers.users_rt import router as rt2
from auth_f.auth_main import router as rt3
from contextlib import asynccontextmanager
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router=rt1)
app.include_router(router=rt2)
app.include_router(router=rt3)
active_connections = []
chats = {}


@app.get('/')
async def welcome():
    return {"message": 'Hello, world!!!'}


@app.get('/health')
async def health_check():
    return {"status": "ok"}


@app.websocket("/webtest")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    chats[1] = websocket
    while True:
        data = await websocket.receive_text()
        data = data.lower()
        await websocket.send_text(f"Получено: {data}!")
        await asyncio.sleep(2)
        await websocket.send_text(f'{data}')
        await asyncio.sleep(1)


@app.websocket("/webtest2")
async def websocket_endpoint2(websocket: WebSocket):
    chats[2] = websocket
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await chats[1].send_text(data)


async def broadcast_message(message: str):
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")

# Пример фоновой задачи, имитирующей получение сообщений от брокера

# async def broker_listener():
#     async for message in ManageBroker.subscribe('devices/1/control'):
#         print(f'MESSAGE: {message}')
#         await asyncio.sleep(2)
#         await broadcast_message(message)
#
#
# asyncio.create_task(broker_listener())
