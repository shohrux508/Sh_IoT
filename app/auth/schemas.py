from pydantic import BaseModel, EmailStr, model_validator, root_validator, field_validator

from app.auth.utils import hash_password


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str

    @field_validator('hashed_password')
    def hash_psw(cls, value):
        return hash_password(value)


class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
