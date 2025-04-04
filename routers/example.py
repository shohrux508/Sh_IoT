from fastapi import APIRouter
from schemas import Device

router = APIRouter(prefix='/devices', tags=['Devices'])


@router.get('/')
async def get_devices():
    return [{'id': 1}]


@router.post('/')
async def add_device(device: Device):
    print(Device)
    return {'message': "success"}

