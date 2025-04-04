from database.engine import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import TypeVar


class Device(Base):
    __tablename__ = 'devices'
    id: Mapped[int] = mapped_column(unique=True)


class Client(Base):
    __tablename__ = 'clients'
    id: Mapped[int] = mapped_column(unique=True)


ModelType = TypeVar('ModelType', bound=Base)
