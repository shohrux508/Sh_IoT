from auth_f.pwd_hash import hash_password
from database.models import User, Device, ModelType
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, insert

from schemas.schemas import UserCreate, DeviceCreate


class DB:
    def __init__(self, model: type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, model_id: int = None):
        statement = select(self.model)
        if model_id:
            statement = statement.where(self.model.pk == model_id)
        response = await self.session.execute(statement)
        response = response.scalars().all() if model_id else response.scalar_one()
        return response

    async def delete(self, model_id: int):
        statement = delete(self.model).where(self.model.id == model_id)
        await self.session.execute(statement)
        await self.session.commit()


class Devices(DB):
    def __init__(self, session: AsyncSession):
        super().__init__(Device, session)

    async def create(self, device: DeviceCreate):
        stmt = insert(Device).values(
            id=device.id,
            name=device.name
        ).returning(Device)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()


class Users(DB):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def create(self, user: UserCreate):
        stmt = insert(User).values(
            username=user.username,
            email=user.email,
            hashed_password=await hash_password(user.password)
        ).returning(User)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()
