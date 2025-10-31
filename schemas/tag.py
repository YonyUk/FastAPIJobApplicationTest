from typing import Annotated
from pydantic import BaseModel
from pydantic.types import StringConstraints
from .mixins import TimestampSchema

class TagBaseSchema(BaseModel):
    '''
    base schema for 'Tag'
    '''
    name:Annotated[str,StringConstraints(min_length=2,max_length=10)]
    description:Annotated[str,StringConstraints(min_length=2,max_length=255)]

class TagCreateSchema(TagBaseSchema):
    '''
    schema for create a tag
    '''

class TagUpdateSchema(TagBaseSchema):
    '''
    schema to update a tag
    '''

class TagSchema(TagBaseSchema,TimestampSchema):
    '''
    schema for tags
    '''
    id:str