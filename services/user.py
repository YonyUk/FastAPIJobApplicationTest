from repositories import UserRepository
from models import User
from schemas import UserCreateSchema
from settings import ENVIRONMENT

class UserService:

    def __init__(self,user_repository:UserRepository):
        '''
        service for the 'User' entity
        '''
        self._repository = user_repository
        self._crypt_context = ENVIRONMENT.CRYPT_CONTEXT
    
    # gets the user instance
    def _get_user_instance(
        self,
        user:UserCreateSchema,
        user_id:str | None = None
    ) -> User:
        db_user = User(
            id=user_id,
            username=user.username,
            email=user.email,
            hashed_password=self._crypt_context.hash(str(user.password))
        )
        return db_user
    
    async def authenticate_user(self,username:str,password:str) -> User | None:
        '''
        authenticates a user

        returns None if the user wasn't authenticated
        '''
        user = await self._repository.get_by_username(username)
        if not user:
            return None
        if not self._crypt_context.verify(password,user.hashed_password):
            return None
        return user
    
    async def create(self,user:UserCreateSchema) -> User | None:
        '''
        creates a new 'User' in the repository

        returns None if the user wasn't created
        '''
        db_user = self._get_user_instance(user)
        return await self._repository.create(db_user)
    
    async def get_by_username(self,username:str) -> User | None:
        '''
        gets a user by his username
        '''
        return await self._repository.get_by_username(username)
    
    async def get_by_id(self,user_id:str) -> User | None:
        '''
        gets a user by his id
        '''
        return await self._repository.get_by_id(user_id)
    
    async def get_by_email(self,email:str) -> User | None:
        '''
        gets a user by his email
        '''
        return await self._repository.get_by_email(email)