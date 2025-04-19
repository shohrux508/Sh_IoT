from fastapi import Depends, APIRouter
from app.users.dependencies import get_user_service
from app.auth.schemas import UserRead, UserCreate
from app.users.service import UserService

router = APIRouter(prefix='/auth', tags=['Авторизация'])


@router.post('/register', response_model=UserRead, summary='Зарегистрироваться')
async def register_user(user: UserCreate, users_db: UserService = Depends(get_user_service)):
    response = await users_db.create(user)
    return UserRead(id=response.id, email=response.email)

