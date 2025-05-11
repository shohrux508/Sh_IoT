from app.devices.repositories import DevicesRepository
from app.services import BaseService


class DeviceService(BaseService[DevicesRepository]):
    def __init__(self, repo: DevicesRepository):
        super().__init__(repo)
        self.repo = repo

