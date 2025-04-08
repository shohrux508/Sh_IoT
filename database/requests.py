from database.models import User, Device, ModelType
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, insert


class DB:
    def __init__(self, model: type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, model_id: int = None):
        statement = select(self.model)
        if model_id:
            statement = statement.where(self.model.id == model_id)
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

    async def create(self, device_name: str, device_id: int):
        statement = insert(self.model).values(id=device_id, name=device_name)
        await self.session.execute(statement)
        await self.session.commit()

    # async def update(self, pk: int, device_id: int):
    #     statement = update(Device).where(Device.pk == pk).values(device_id=device_id)
    #     await self.session.execute(statement)
    #     await self.session.commit()


class Users(DB):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    # async def update(self, pk: int, client_id: int):
    #     statement = update(Client).where(Client.pk == pk).values(client_id=client_id)
    #     await self.session.execute(statement)
    #     await self.session.commit()
