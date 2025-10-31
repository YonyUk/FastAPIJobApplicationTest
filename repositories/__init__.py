from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import get_database_session
from .user import UserRepository
from .post import PostRepository
from .comment import CommentRepository

def get_user_repository(db:AsyncSession=Depends(get_database_session)):
    '''
    gets the 'UserRepository' dependency
    '''
    repository = UserRepository(db)
    try:
        yield repository
    finally:
        repository = None

def get_post_repository(db:AsyncSession=Depends(get_database_session)):
    '''
    gets the 'PostRepository' dependency
    '''
    repository  = PostRepository(db)
    try:
        yield repository
    finally:
        repository = None

def get_comment_repository(db:AsyncSession=Depends(get_database_session)):
    '''
    gets the 'CommentRepository' dependency
    '''
    repository = CommentRepository(db)
    try:
        yield repository
    finally:
        repository = None