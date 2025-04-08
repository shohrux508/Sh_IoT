from database.engine import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import TypeVar


class Device(Base):
    __tablename__ = 'devices'
    id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()


ModelType = TypeVar('ModelType', bound=Base)
