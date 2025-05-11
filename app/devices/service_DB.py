from app.devices.repository_DB import DeviceRepository
from app.services import BaseService


class DeviceService(BaseService[DeviceRepository]):
    def __init__(self, repo: DeviceRepository):
        super().__init__(repo)

    async def list_all(self):
        return await self.repo.get_all_devices()

    async def list_filtered_sorted(self, name: str = None, sort: str = None):
        return await self.repo.get_filtered_sorted(name=name, sort=sort)


