from app.orders.database.repositories import OrderRepository
from app.services import BaseService

class OrderService(BaseService[OrderRepository]):
    def __init__(self, db_repository: OrderRepository):
        super.__init__()