from models import User

class AuthorizationService:

    def __init__(self,user:User):
        '''
        authorization service for permissions managmente based on
        resource owner
        '''
        self._user = user

    def _validate_ownership(
        self,
        resource_owner_id:str,
    ) -> bool:
        return resource_owner_id == self._user.id
    
    def validate_modification(
        self,
        resource_owner_id:str
    ) -> bool:
        return self._validate_ownership(resource_owner_id)
    
    def validate_deletion(
        self,
        resource_owner_id:str
    ) -> bool:
        return self._validate_ownership(resource_owner_id)