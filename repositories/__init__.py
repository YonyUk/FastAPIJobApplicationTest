from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import get_database_session
from .user import UserRepository

def get_user_repository(db:AsyncSession=Depends(get_database_session)):
    '''
    gets the 'UserRepository' dependency
    '''
    repository = UserRepository(db)
    try:
        yield repository
    finally:
        repository = None