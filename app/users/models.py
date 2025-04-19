from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class User(Base):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
