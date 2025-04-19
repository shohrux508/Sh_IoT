from app.services import BaseService
from app.users.repositories import UserRepository


class UserService(BaseService[UserRepository]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository)
        self.user_repository = user_repository
    
    