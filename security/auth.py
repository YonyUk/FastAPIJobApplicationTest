import jwt
from jwt import PyJWTError
from datetime import datetime,timedelta
import datetime as dt
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from models import User
from schemas import TokenDataSchema
from settings import ENVIRONMENT
from services import UserService,get_user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{ENVIRONMENT.GLOBAL_API_PREFIX}/users/token')

def create_access_token(data:dict,expires_delta:timedelta | None = None) -> str:
    '''
    creates a new access token
    '''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(dt.timezone.utc) + expires_delta
    else:
        expire = datetime.now(dt.timezone.utc) + timedelta(minutes=ENVIRONMENT.TOKEN_LIFE_TIME)
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode,ENVIRONMENT.SECRET_KEY,algorithm=ENVIRONMENT.ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token:str = Depends(oauth2_scheme),
    service:UserService = Depends(get_user_service)
) -> User:
    '''
    gets the current user from the authorization token
    '''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate':'Bearer'}
    )
    try:
        payload = jwt.decode(token,ENVIRONMENT.SECRET_KEY,algorithms=[ENVIRONMENT.ALGORITHM])
        username:str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenDataSchema(username=username)
    except PyJWTError:
        raise credentials_exception
    
    user = await service.get_by_username(username)
    if user is None:
        raise credentials_exception
    return user