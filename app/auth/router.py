from fastapi import APIRouter, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
from app.auth.schemas import UserCreate, UserLogin
from app.auth.utils import hash_password, verify_password

router = APIRouter(prefix='/auth')

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ['cookies']

security = AuthX(config=config)

@router.post('/register')
async def register(creds: UserCreate):
    pw = creds.password
    username = creds.username
    email = creds.email



@router.post("/login")
async def login(creds: UserLogin, response: Response):
    hashed_pw = hash_password(creds.password)
    if creds.username == 'test' and verify_password(plain_password=creds.password, hashed_password=hashed_pw):
        token = security.create_access_token(uid='12345')
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail='Incorrect username of password')

@router.get('/protected', dependencies=[Depends(security.access_token_required)])
def protected():
    return {"data": "HELLO, WORLD!"}
