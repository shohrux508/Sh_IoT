from pydantic import BaseModel


class Device(BaseModel):
    id: int


class DeviceOut(Device):
    pass


class DeviceCreate(Device):
    name: str
