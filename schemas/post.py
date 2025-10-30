from typing import Annotated
from pydantic import BaseModel
from pydantic.types import StringConstraints
from settings import ENVIRONMENT
from .mixins import TimestampSchema

class PostBaseSchema(BaseModel):
    '''
    base schema for 'Post'
    '''
    title:Annotated[str,StringConstraints(min_length=ENVIRONMENT.MIN_POST_TITLE_LENGTH, max_length=ENVIRONMENT.MAX_POST_TITLE_LENGTH)]
    content:Annotated[str,StringConstraints(min_length=1)]
    author_name:Annotated[str,StringConstraints(min_length=ENVIRONMENT.MIN_USERNAME_LENGTH,max_length=ENVIRONMENT.MAX_USERNAME_LENGTH)]

class PostSchema(PostBaseSchema,TimestampSchema):
    '''
    schema for 'Post'
    '''