import asyncio
import sys
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
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
async def lifespan(app1: FastAPI):
    from app.events import handlers
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(main_router)

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/devices/emulation', response_class=HTMLResponse)
async def device_emulation(request: Request):
    return templates.TemplateResponse('device_emulation.html', {"request": request})


@app.get('/admin', response_class=HTMLResponse)
async def admin_panel(request: Request):
    return templates.TemplateResponse('admin_panel.html', {"request": request})


@app.middleware('http')
async def log_requests(request: Request, call_next):
    client = request.client.host if request.client else 'unknown'
    print(f"Запрос от: {client}")
    response = await call_next(request)
    print("Ответ отправлен")
    return response
