from pydantic import BaseModel
from datetime import datetime

class TimestampSchema(BaseModel):
    '''
    mixin schema for 'Timestamp'
    '''
    created_at:datetime
    updated_at:datetime