from sys import prefix

from fastapi import APIRouter
from database.engine import async_session
from schemas import UserOut, UserCreate

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/')
async def get_users():
    return {"id": 1}


@router.post("")
async def create_user():
    return {"message": "success"}
