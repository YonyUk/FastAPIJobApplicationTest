from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update
from models import User
from .base import BaseRepository

class UserRepository(BaseRepository):

    def __init__(self,db:AsyncSession):
        '''
        repository for 'User' entity
        '''
        super().__init__(User,db)
    
    async def _get_instance_ignore_deleted(self, instance: User) -> User | None:
        if not instance.id is None:
            return await self.get_by_id(instance.id,True)
        if not instance.username is None:
            return await self.get_by_username(instance.username,True)
        if not instance.email is None:
            return await self.get_by_email(instance.email,True)

    async def get_by_username(self,username:str,include_deleted:bool=False) -> User | None:
        '''
        gets a user by his username
        '''
        query = select(User)
        if include_deleted:
            query = query.where(User.username==username)
        else:
            query = query.where((User.username==username) & (User.is_deleted != True))
        result = await self._db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_email(self,email:str,include_deleted:bool=False) -> User | None:
        '''
        gets a user by his email
        '''
        query = select(User)
        if include_deleted:
            query = query.where(User.email==email)
        else:
            query = query.where((User.email==email) & (User.is_deleted != True))
        result = await self._db.execute(query)
        return result.scalar_one_or_none()