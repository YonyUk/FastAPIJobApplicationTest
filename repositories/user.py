from typing import List, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Result, Tuple, select,update
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

    async def get_user_ignore_deleted(self,user:User) -> User | None:
        '''
        gets a user for any of his unique fields ignoring if he was deleted
        '''
        result = None
        if not user.id is None:
            result = await self._db.execute(
                select(User).where(User.id == user.id)
            )
        elif not user.username is None:
            result = await self._db.execute(
                select(User).where(User.username == user.username)
            )
        else:
            result = await self._db.execute(
                select(User).where(User.email==user.email)
            )
        return result.scalar_one_or_none()

    async def get_by_id_ignore_deleted(self,user_id:str) -> User | None:
        '''
        gets a user by his id ignoring if he was deleted
        '''
        result = await self._db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_username_ignore_deleted(self,username:str) -> User | None:
        '''
        gets a user by his username ignoring if he was deleted
        '''
        result = await self._db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self,user_id:str) -> User | None:
        '''
        gets a user by his id
        '''
        result = await self._db.execute(
            select(User).where((User.id==user_id) & (User.is_deleted != True))
        )
        return result.scalar_one_or_none()

    async def get_by_username(self,username:str) -> User | None:
        '''
        gets a user by his username
        '''
        result = await self._db.execute(
            select(User).where((User.is_deleted != True) & (User.username==username))
        )
        return result.scalar_one_or_none()
    
    async def get_by_email(self,email:str) -> User | None:
        '''
        gets a user by his email
        '''
        result = await self._db.execute(
            select(User).where((User.email==email) & (User.is_deleted != True))
        )
        return result.scalar_one_or_none()
    
    async def get_all(self) -> Sequence[User]:
        '''
        gets all the users
        '''
        result = await self._db.execute(
            select(User).where(User.is_deleted != True)
        )
        return result.scalars().all()
    
    async def create(self,user:User) -> User | None:
        '''
        creates a new User in the database

        returns None if the user wasn't created
        '''
        db_user = await self.get_user_ignore_deleted(user)
        if not db_user:
            self._db.add(user)
            await self._db.commit()
            await self._db.refresh(user)
            return user
        elif db_user.is_deleted:
            db_user.is_deleted = False
            update_data = self._user_to_dict(db_user)
            await self._db.execute(
                update(User).where(User.id==db_user.id).values(**update_data)
            )
            await self._db.commit()
            await self._db.refresh(db_user)
            return db_user
        else:
            return None
    
    async def update(self,user_id:str,user_update:User) -> User | None:
        '''
        updates a 'User' in the database
        '''
        db_user = await self.get_by_id(user_id)
        if db_user is None:
            return None
        
        user_update.created_at = db_user.created_at
        user_update.updated_at = db_user.updated_at
        update_data = self._user_to_dict(user_update)
        await self._db.execute(
            update(User).where((User.id==user_id) & (User.is_deleted != True)).values(**update_data)
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