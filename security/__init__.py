from fastapi import Depends
from models import User
from services import AuthorizationService
from .auth import get_current_user,create_access_token

def get_authorization_service(user:User=Depends(get_current_user)):
    service = AuthorizationService(user)
    try:
        yield service
    finally:
        service = None