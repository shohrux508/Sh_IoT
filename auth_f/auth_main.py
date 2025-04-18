from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_session
from database.models import User
from database.requests import Users
from schemas.schemas import UserRead, UserCreate

router = APIRouter(prefix='/auth')


@router.post('/register', response_model=UserRead, tags=['Регистрация'], summary='Зарегистрироваться')
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    response = await Users(session).create(user)
    print(await Users(session).get())
    return UserRead(pk=response.pk, email=response.email)

