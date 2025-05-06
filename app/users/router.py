from fastapi import APIRouter, Depends

from app.users.dependencies import get_user_service
from app.users.service import UserService

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get('/', name='Список пользователей')
async def get_users(service: UserService = Depends(get_user_service)):
    await service.get_by_id()
    return {"device_id": 1}
