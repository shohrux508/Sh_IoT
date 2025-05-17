from fastapi import APIRouter

from app.devices.device_routers import router as devices_router

main_router = APIRouter()

main_router.include_router(devices_router)
