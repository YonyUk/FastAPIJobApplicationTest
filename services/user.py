from typing import Sequence
from repositories import UserRepository
from models import User
from schemas import UserCreateSchema,UserUpdateSchema,UserSchema
from settings import ENVIRONMENT
from .base import BaseService

# class UserService:

#     def __init__(self,user_repository:UserRepository):
#         '''
#         service for the 'User' entity
#         '''
#         self._repository = user_repository
#         self._crypt_context = ENVIRONMENT.CRYPT_CONTEXT
    
#     # gets the user instance
#     def _get_user_instance(
#         self,
#         user:UserCreateSchema | UserUpdateSchema,
#         user_id:str | None = None
#     ) -> User:
        
#         return User(
#             id=user_id,
#             username=user.username,
#             email=user.email,
#             hashed_password=self._crypt_context.hash(user.password)
#         )
    
#     async def authenticate_user(self,username:str,password:str) -> UserSchema | None:
#         '''
#         authenticates a user

#         returns None if the user wasn't authenticated
#         '''
#         user = await self._repository.get_by_username(username)
#         if not user:
#             return None
#         if not self._crypt_context.verify(password,user.hashed_password):
#             return None
#         return user
    
#     async def create(self,user:UserCreateSchema) -> UserSchema | None:
#         '''
#         creates a new 'User' in the repository

#         returns None if the user wasn't created
#         '''
#         db_user = self._get_user_instance(user)
#         return await self._repository.create(db_user)
    
#     async def get_by_username(self,username:str) -> UserSchema | None:
#         '''
#         gets a user by his username
#         '''
#         return await self._repository.get_by_username(username)
    
#     async def get_by_id(self,user_id:str) -> UserSchema | None:
#         '''
#         gets a user by his id
#         '''
#         return await self._repository.get_by_id(user_id)
    
#     async def get_by_email(self,email:str) -> UserSchema | None:
#         '''
#         gets a user by his email
#         '''
#         return await self._repository.get_by_email(email)
    
#     async def get_all(self) -> Sequence[UserSchema]:
#         '''
#         gets all the users
#         '''
#         return await self._repository.get_all()
    
#     async def update(self,user_id:str,user_update:UserUpdateSchema) -> User | None:
#         '''
#         updates a user
#         '''
#         user = await self._repository.get_by_id(user_id)
#         if user is None:
#             return None
        
#         db_user = self._get_user_instance(user_update,user_id)
#         db_user.created_at = user.created_at
#         db_user.updated_at = user.updated_at
#         db_user.is_deleted = user.is_deleted
#         return await self._repository.update(user_id,db_user)
    
#     async def delete(self,user_id:str) -> bool:
#         '''
#         deletes a user
#         '''
#         return await self._repository.delete(user_id)

class UserService(
    BaseService[
        User,
        UserCreateSchema,
        UserUpdateSchema,
        UserSchema,
        UserRepository
    ]
):
    
    def __init__(self,user_repository:UserRepository):
        '''
        repository for 'User'
        '''
        super().__init__(User,user_repository)
        self._crypt_context = ENVIRONMENT.CRYPT_CONTEXT
    
    def _get_instance(self, **fields) -> User:
        password = fields['password']
        fields['hashed_password'] = self._crypt_context.hash(password)
        del fields['password']
        return super()._get_instance(**fields)
    
    async def _process_before_update_modifier(
        self,
        update_data: UserUpdateSchema,
        existing_model: User,
        model: User
    ) -> User:
        model.created_at = existing_model.created_at
        model.updated_at = existing_model.updated_at
        model.is_deleted = existing_model.is_deleted
        return model
    
    async def authenticate_user(self,username:str,password:str) -> User | None:
        '''
        authenticate a user
        '''
        user = await self._repository.get_by_username(username)
        if user is None:
            return None
        if not self._crypt_context.verify(password,user.hashed_password):
            return None
        return user

    async def get_by_username(self,username:str,include_deleted:bool=False) -> UserSchema | None:
        '''
        gets a user by his username
        '''
        return await self._repository.get_by_username(username,include_deleted)
    
    async def get_by_email(self,email:str,include_deleted:bool=False) -> UserSchema | None:
        '''
        gets a user by his username
        '''
        return await self._repository.get_by_email(email,include_deleted)