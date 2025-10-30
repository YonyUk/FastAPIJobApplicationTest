from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update
from models import User

class UserRepository:

    def __init__(self,db:AsyncSession):
        '''
        database repository for 'User' entity
        '''
        self._db = db
    
    def _user_to_dict(self,user:User) -> dict:
        return {
            'id':user.id,
            'username':user.username,
            'email':user.email,
            'hashed_password':user.hashed_password,
            'created_at':user.created_at,
            'updated_at':user.updated_at,
            'is_deleted':user.is_deleted if user.is_deleted is not None else False,
            'deleted_at':user.deleted_at
        }

    async def get_by_id(self,user_id:str) -> User | None:
        '''
        gets a user by his id
        '''
        result = await self._db.execute(
            select(User).where(User.id==user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self,username:str) -> User | None:
        '''
        gets a user by his username
        '''
        result = await self._db.execute(
            select(User).where(User.username==username)
        )
        return result.scalar_one_or_none()
    
    async def get_by_email(self,email:str) -> User | None:
        '''
        gets a user by his email
        '''
        result = await self._db.execute(
            select(User).where(User.email==email)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self) -> List[User]:
        '''
        gets all the users
        '''
        result = await self._db.execute(
            select(User)
        )
        return list(result.scalars().all())
    
    async def create(self,user:User) -> User | None:
        '''
        creates a new User in the database

        returns None if the user wasn't created
        '''
        db_user = await self.get_by_id(user.id)
        if not db_user:
            self._db.add(user)
            await self._db.commit()
            await self._db.refresh(user)
            return user
        return None
    
    async def update(self,user_id:str,user_update:User) -> User | None:
        '''
        updates a 'User' in the database
        '''
        db_user = await self.get_by_id(user_id)
        if db_user is None:
            return None
        
        update_data = self._user_to_dict(user_update)
        await self._db.execute(
            update(User).where(User.id==user_id).values(**update_data)
        )
        await self._db.commit()
        await self._db.refresh(db_user)

        return db_user
    
    async def delete(self,user_id:str) -> bool:
        '''
        deletes a 'User'
        '''
        db_user = await self.get_by_id(user_id)
        if db_user is None:
            return False
        db_user.soft_delete()
        await self._db.commit()
        await self._db.refresh(db_user)

        return True