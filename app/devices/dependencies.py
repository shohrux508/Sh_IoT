from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.devices.service_DB import DeviceService
from app.devices.repository_DB import DeviceRepository


def get_device_repository(db: AsyncSession = Depends(get_db)) -> DeviceRepository:
    return DeviceRepository(db)


def get_device_service(repo: DeviceRepository = Depends(get_device_repository)) -> DeviceService:
    return DeviceService(repo)
