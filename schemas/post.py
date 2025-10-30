from typing import Annotated
from pydantic import BaseModel
from pydantic.types import StringConstraints
from settings import ENVIRONMENT

class PostBaseSchema(BaseModel):
    '''
    base schema for 'Post'
    '''
    title:Annotated[str,StringConstraints(min_length=ENVIRONMENT.MIN_POST_TITLE_LENGTH, max_length=ENVIRONMENT.MAX_POST_TITLE_LENGTH)]