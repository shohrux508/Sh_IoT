from fastapi import APIRouter

from app.auth.router import router as auth_router
from app.devices.router import router as devices_router
from app.users.router import router as users_router

main_router = APIRouter()

main_router.include_router(auth_router)
main_router.include_router(users_router)
main_router.include_router(devices_router)
