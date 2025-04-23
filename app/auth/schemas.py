from pydantic import BaseModel, EmailStr, model_validator, root_validator, field_validator

from app.auth.utils import hash_password


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator('password')
    def hash_psw(self, value):
        return hash_password(value)

class UserLogin(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
