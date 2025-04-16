from pydantic import BaseModel, EmailStr


class DeviceOut(BaseModel):
    id: int


class DeviceCreate(BaseModel):
    id: int
    name: str


class UserOut(BaseModel):
    id: int


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    pk: int
    email: EmailStr

    class Config:
        from_attributes = True
