from sqlalchemy.ext.asyncio import AsyncSession

from app.devices.models import Device
from app.repositories import BaseRepository


class Devices(BaseRepository[Device]):
    def __init__(self, session: AsyncSession):
        super().__init__(Device, session)
