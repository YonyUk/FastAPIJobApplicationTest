from pydantic import BaseModel,EmailStr
from typing import Annotated
from pydantic.types import StringConstraints
from settings import ENVIRONMENT

class UserBaseSchema(BaseModel):
    '''
    base schema for 'User'
    '''
    username:Annotated[str,StringConstraints(min_length=ENVIRONMENT.MIN_USERNAME_LENGTH, max_length=ENVIRONMENT.MAX_USERNAME_LENGTH)]
    email:EmailStr

class UserCreateSchema(UserBaseSchema):
    '''
    schema for create 'User'
    '''
    password:Annotated[str,StringConstraints(min_length=ENVIRONMENT.MIN_USER_PASSWORD_LENGTH, max_length=ENVIRONMENT.MAX_USER_PASSWORD_LENGTH)]

class UserSchema(UserBaseSchema):
    '''
    schema for 'User'
    '''
    id:str

    class Config:
        orm_mode = True