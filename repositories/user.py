from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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

    async def get_by_username(self,username:str) -> User | None:
        '''
        gets a user by his username
        '''
        result = await self._db.execute(
            select(User).where(User.username==username)
        )
        return result.scalars().first()
    
    async def get_by_email(self,email:str) -> User | None:
        '''
        gets a user by his email
        '''
        result = await self._db.execute(
            select(User).where(User.email==email)
        )
        return result.scalars().first()
    
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