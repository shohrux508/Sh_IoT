from pydantic import BaseModel, constr


class DeviceControl_request(BaseModel):
    device_type: str
    state: bool | int | None = None
    start_time: constr(pattern=r"^\d{2}:\d{2}$") | None = None
    stop_time: constr(pattern=r"^\d{2}:\d{2}$") | None = None


class DeviceCreate(BaseModel):
    name: str


class DeviceDataInfo(BaseModel):
    registration_code: str
    auth_token: str

    class Config:
        from_attributes = True


class DeviceInfo(BaseModel):
    id: int
    name: str
    last_seen: str | None = None
    data: DeviceDataInfo

    class Config:
        from_attributes = True


class DeviceControl_response(BaseModel):
    action: str
    state: bool | int
    device_id: int


class DeviceStatus_response(BaseModel):
    device_id: int
    state: bool


class Device(BaseModel):
    device_id: int


class CommandResponse(Device):
    success: bool
    command: str


class ErrorResponse(BaseModel):
    error: str


class ActiveDevicesResponse(BaseModel):
    active_devices: list[int]

    class Config:
        arbitrary_types_allowed = True
