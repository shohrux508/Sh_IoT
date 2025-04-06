from pydantic import BaseModel



class DeviceOut(BaseModel):
    id: int


class DeviceCreate(BaseModel):
    id: int
    name: str


class UserOut(BaseModel):
    id: int


class UserCreate(BaseModel):
    name: str
