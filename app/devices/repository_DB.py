from app.repositories import BaseRepository
from app.devices.models import Device
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import datetime
from typing import List, Sequence


class DeviceRepository(BaseRepository[Device]):
    def __init__(self, session: AsyncSession):
        super().__init__(Device, session)

    async def get_by_registration_code(self, code: str) -> Device | None:
        result = await self.session.execute(
            select(Device).where(Device.registration_code == code)
        )
        return result.scalar_one_or_none()

    async def mark_as_registered(self, device: Device):
        device.is_registered = True
        device.registered_at = datetime.datetime.now()
        await self.session.commit()

    async def get_by_auth_token(self, auth_token: str) -> Device:
        stmt = select(Device).where(Device.auth_token == auth_token)
        result = await self.session.execute(stmt)
        device = result.scalar_one_or_none()
        return device

    async def get_all_devices(self) -> Sequence[Device]:
        stmt = select(Device)
        result = await self.session.execute(stmt)
        devices = result.scalars().all()
        return devices
