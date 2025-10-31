from typing import Annotated,Optional,Sequence
from pydantic import BaseModel, EmailStr
from pydantic.types import StringConstraints
from settings import ENVIRONMENT
from .mixins import TimestampSchema

class PostUserNestedSchema(BaseModel):
    '''
    schema for users relation
    '''
    username:Annotated[
        str,
        StringConstraints(
            min_length=ENVIRONMENT.MIN_USERNAME_LENGTH,
            max_length=ENVIRONMENT.MAX_USERNAME_LENGTH
        )
    ]
    email:EmailStr

class PostTagNestedSchema(BaseModel):
    '''
    schema for tags relation
    '''
    name:Annotated[str,StringConstraints(min_length=2,max_length=10)]
    description:Annotated[str,StringConstraints(min_length=2,max_length=255)]

class PostCommentNestedSchema(BaseModel):
    '''
    schema for comments relation
    '''
    content:Annotated[str,StringConstraints(min_length=1,max_length=255)]
    author:Annotated[
        str,
        StringConstraints(
            min_length=ENVIRONMENT.MIN_USERNAME_LENGTH,
            max_length=ENVIRONMENT.MAX_USERNAME_LENGTH
        )
    ]

class PostBaseSchema(BaseModel):
    '''
    base schema for 'Post'
    '''
    title:Annotated[
        str,
        StringConstraints(
            min_length=ENVIRONMENT.MIN_POST_TITLE_LENGTH,
            max_length=ENVIRONMENT.MAX_POST_TITLE_LENGTH
        )
    ]
    content:Annotated[str,StringConstraints(min_length=1)]

class PostCreateSchema(PostBaseSchema):
    '''
    schema for create post
    '''
    tags:Optional[Sequence[PostTagNestedSchema]]

class PostUpdateSchema(PostBaseSchema):
    '''
    schema for update post
    '''
    tags:Optional[Sequence[PostTagNestedSchema]]

class PostSchema(PostBaseSchema,TimestampSchema):
    '''
    schema for 'Post'
    '''
    id:str
    author_id:str
    tags:Optional[Sequence[PostTagNestedSchema]]
    comments:Optional[Sequence[PostCommentNestedSchema]]
    
    class Config:
        orm_mode = True