from pydantic import BaseModel,EmailStr

class UserBaseSchema(BaseModel):
    '''
    base schema for 'User'
    '''
    username:str
    email:EmailStr

class UserCreateSchema(UserBaseSchema):
    '''
    schema for create 'User'
    '''
    password:str

class UserUpdateSchema(UserCreateSchema):
    '''
    schema for update 'User'
    '''

class UserSchema(UserBaseSchema):
    '''
    schema for 'User'
    '''
    id:str

    class Config:
        orm_mode = True