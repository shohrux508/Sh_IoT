from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import BaseRepository
from app.users.models import User


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)
