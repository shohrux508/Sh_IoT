from pydantic import BaseModel, constr


class DeviceRequestControl(BaseModel):
    device_type: str
    state: bool | int | None = None
    start_time: constr(pattern=r"^\d{2}:\d{2}$") | None = None
    stop_time: constr(pattern=r"^\d{2}:\d{2}$") | None = None


class DeviceControlResponse(BaseModel):
    action: str
    state: bool | int
    device_id: int


class DeviceStatusResponse(BaseModel):
    device_id: int
    state: bool


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
