from fastapi import APIRouter

router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get('/', name='Список пользователей')
async def get_users():
    return {"device_id": 1}
