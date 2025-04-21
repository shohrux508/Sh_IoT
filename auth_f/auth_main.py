from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_session
from database.models import User
from database.requests import Users
from schemas.schemas import UserRead, UserCreate
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext


SECRET_KEY = "key"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


router = APIRouter(prefix='/auth')


@router.post('/register', response_model=UserRead, tags=['Регистрация'], summary='Зарегистрироваться')
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    response = await Users(session).create(user)
    print(await Users(session).get())
    return UserRead(pk=response.pk, email=response.email)

