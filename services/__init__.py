from fastapi import Depends
from repositories import get_user_repository,UserRepository
from .user import UserService

def get_user_service(repository:UserRepository = Depends(get_user_repository)):
    '''
    gets the user service dependency
    '''
    service = UserService(repository)
    try:
        yield service
    finally:
        service = None