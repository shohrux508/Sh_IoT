import asyncio
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, Request

from app import main_router
from app.database import init_db

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(main_router)


@app.get('/')
async def welcome():
    return {"message": 'Hello, world!!!'}


@app.get('/health')
async def health_check():
    return {"status": "ok"}


@app.middleware('http')
async def log_requests(request: Request, call_next):
    print(f"Запрос от: {request.client.host}")
    response = await call_next(request)
    print("Ответ отправлен")
    return response
