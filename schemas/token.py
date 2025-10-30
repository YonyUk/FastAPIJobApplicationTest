from pydantic import BaseModel

class TokenSchema(BaseModel):
    '''
    schema for an access token
    '''
    access_token:str
    token_type:str

class TokenDataSchema(BaseModel):
    '''
    schema for the token's data
    '''
    username:str | None = None