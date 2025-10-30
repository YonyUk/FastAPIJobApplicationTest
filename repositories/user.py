from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update
from models import User
from settings import ENVIRONMENT

class UserRepository:

    def __init__(self,db:AsyncSession):
        '''
        database repository for 'User' entity
        '''
        self._db = db
        self._crypt_context = ENVIRONMENT.CRYPT_CONTEXT
    
    def _user_to_dict(self,user:User) -> dict:
        return {
            'id':user.id,
            'username':user.username,
            'email':user.email,
            'hashed_password':user.hashed_password,
            'admin':user.admin
        }
    
    async def get_by_id(self,user_id:str) -> User | None:
        '''
        gets a user by his id
        '''
        result = await self._db.execute(
            select(User).where(User.id==user_id)
        )
        return result.scalars().first()

    async def create(self,user:User) -> User:
        '''
        creates a new User in the database
        '''
        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)
        return user
    
    async def update(self,user_id:str,user_update:User) -> User | None:
        '''
        updates the data for the user with the given id and the new given data
        '''
        user = await self.get_by_id(user_id)
        if user is None:
            return None
        
        update_data = self._user_to_dict(user_update)
        if not update_data is None:
            await self._db.execute(
                update(User).where(User.id==user_id).values(**update_data)
            )
            await self._db.commit()
            await self._db.refresh(user)
        
        return user
    
    async def delete(self,user_id:str) -> bool:
        '''
        deletes a user by his id
        '''
        user = self.get_by_id(user_id)
        if user is None:
            return False
        
        await self._db.delete(user)
        await self._db.commit()
        return True
    
    async def get_all(self,limit:int=100,skip:int=0) -> List[User]:
        '''
        gets all the users

        params:

            limit:int -> max number of results in the response
            skip:int -> number of registers to skip
        '''
        result = await self._db.execute(
            select(User).offset(skip).limit(limit)
        )
        return list(result.scalars().all())