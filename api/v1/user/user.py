from typing import List
from fastapi import APIRouter,HTTPException,status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from models import User
from schemas import UserCreateSchema,UserSchema,TokenSchema,UserUpdateSchema
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
    service:UserService=Depends(get_user_service)
):
    db_user = await service.get_by_username(str(user.username))
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

@router.get(
    '/',
    response_model=List[UserSchema]
)
async def get_users(
    service:UserService=Depends(get_user_service)
):
    return await service.get_all()

@router.get(
    '/{user_id}',
    response_model=UserSchema
)
async def get_by_id(
    user_id:str,
    service:UserService=Depends(get_user_service)
):
    db_user = await service.get_by_id(user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not user with id "{user_id}" found'
        )
    return db_user

@router.get(
    '/username/{username}',
    response_model=UserSchema
)
async def get_by_username(
    username:str,
    service:UserService=Depends(get_user_service)
):
    db_user = await service.get_by_username(username)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not user with username "{username}" found'
        )
    return db_user

@router.get(
    '/email/{email}',
    response_model=UserSchema
)
async def get_by_email(
    email:str,
    service:UserService=Depends(get_user_service)
):
    db_user = await service.get_by_email(email)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not user with email "{email}" found'
        )
    return db_user

@router.put(
    '/update',
    response_model=UserSchema,
    status_code=status.HTTP_202_ACCEPTED
)
async def update_user(
    user_update:UserUpdateSchema,
    service:UserService=Depends(get_user_service),
    current_user:User=Depends(get_current_user)
):
    return await service.update(current_user.id,user_update)

@router.delete(
    '/delete',
    status_code=status.HTTP_202_ACCEPTED
)
async def delete_user(
    service:UserService=Depends(get_user_service),
    current_user:User=Depends(get_current_user)
):
    result = await service.delete(current_user.id)
    return {'messsage':'user deleted' if result else 'user was not deleted'}