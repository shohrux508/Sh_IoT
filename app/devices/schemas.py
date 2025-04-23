from typing import Dict

from pydantic import BaseModel
from fastapi.websockets import WebSocket


class Device(BaseModel):
    device_id: int


class DeviceResponse(Device):
    pass


class DeviceCreate(BaseModel):
    token: str


class CommandResponse(Device):
    success: bool
    command: str

class ErrorResponse(BaseModel):
    error: str

class ActiveDevicesResponse(BaseModel):
    active_devices: list[int]

    class Config:
        arbitrary_types_allowed = True