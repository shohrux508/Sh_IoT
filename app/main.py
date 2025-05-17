import asyncio
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from app import main_router
from app.database import init_db
from app.config import LoggingSettings
from app.logger_module.logger_config import LoggingConfig
import logging

settings = LoggingSettings()  # прочитает .env автоматически
LoggingConfig(settings).setup()


def get_logger(name: str = __name__) -> logging.Logger:
    return logging.getLogger(name)


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.events import handlers
    await init_db()
    yield


# 🔧 создаём функцию
def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(main_router)
    return app


app = create_app()


@app.get('/')
async def welcome():
    return {"message": 'Hello, world!!!'}


@app.get('/health')
async def health_check():
    return {"status": "ok"}


@app.middleware('http')
async def log_requests(request: Request, call_next):
    client = request.client.host if request.client else 'unknown'
    print(f"Запрос от: {client}")
    response = await call_next(request)
    print("Ответ отправлен")
    return response
