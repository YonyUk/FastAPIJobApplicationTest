from typing import Annotated
from pydantic import BaseModel
from pydantic.types import StringConstraints
from settings import ENVIRONMENT
from .mixins import TimestampSchema

class CommentBaseSchema(BaseModel):
    '''
    comment base schema
    '''
    content:Annotated[str,StringConstraints(min_length=1,max_length=255)]

class CommentCreateSchema(CommentBaseSchema):
    '''
    schema for create a comment
    '''

class CommentUpdateSchema(CommentBaseSchema):
    '''
    schema for update a comment
    '''

class CommentSchema(CommentBaseSchema,TimestampSchema):
    '''
    schema for the comment
    '''
    id:str
    author_name:Annotated[str,StringConstraints(min_length=ENVIRONMENT.MIN_USERNAME_LENGTH,max_length=ENVIRONMENT.MAX_USERNAME_LENGTH)]