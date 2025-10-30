from fastapi import APIRouter,HTTPException,status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from models import User
from schemas import UserCreateSchema,UserUpdateSchema,UserSchema,TokenSchema
from security import create_access_token,get_current_user
from settings import ENVIRONMENT
from services import UserService,get_user_service
from .user_http_exceptions import (
    USER_ALREADY_EXISTS_ECXCEPTION,
    EMAIL_ALREADY_REGISTERED_EXCEPTION
)

router = APIRouter(prefix='/users',tags=['users'])

@router.post(
    '/register',
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    user:UserCreateSchema,
    status_code=status.HTTP_201_CREATED,
    service:UserService=Depends(get_user_service)
):
    db_user = await service.get_by_username(user.username)
    if db_user:
        raise USER_ALREADY_EXISTS_ECXCEPTION
    db_user = await service.get_by_email(user.email)
    if db_user:
        raise EMAIL_ALREADY_REGISTERED_EXCEPTION
    db_user = await service.create(user)
    return db_user

@router.post(
    '/token',
    response_model=TokenSchema
)
async def login_for_access_token(
    form_data:OAuth2PasswordRequestForm=Depends(),
    service:UserService=Depends(get_user_service)
):
    user = await service.authenticate_user(form_data.username,form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authorization':'Bearer'}
        )
    access_token_expires = timedelta(minutes=float(ENVIRONMENT.TOKEN_LIFE_TIME))
    access_token = create_access_token(
        data={'sub':user.username},
        expires_delta=access_token_expires
    )
    return {'access_token':access_token,'token_type':'bearer'}