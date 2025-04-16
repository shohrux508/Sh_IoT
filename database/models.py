from database.engine import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from typing import TypeVar


class User(Base):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))


class Device(Base):
    __tablename__ = 'devices'
    id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()


ModelType = TypeVar('ModelType', bound=Base)
