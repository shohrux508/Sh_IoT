from sqlalchemy.ext.asyncio import AsyncSession

from app.orders.database.models import Order
from app.repositories import BaseRepository

class OrderRepository(BaseRepository[Order]):
    def __init__(self, session: AsyncSession):
        super.__init__(model=Order, session=session)
