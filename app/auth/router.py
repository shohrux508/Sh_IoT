from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

from app.auth.schemas import UserRead, UserCreate
from app.users.dependencies import get_user_service
from app.users.repositories import UserRepository
from app.users.service import UserService

SECRET_KEY = "key"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix='/auth')


@router.post('/register', response_model=UserRead, tags=['Регистрация'], summary='Зарегистрироваться')
async def register_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    pass
