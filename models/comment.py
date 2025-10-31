from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column
from uuid import uuid4
from database import BaseModel
from .mixins import TimestampMixin,SoftDeleteMixin

class Comment(BaseModel,TimestampMixin,SoftDeleteMixin):
    '''
    comment entity
    '''
    __tablename__ = 'comments'

    id:Mapped[str] = mapped_column(String,primary_key=True,default=lambda:str(uuid4()))
    author_name:Mapped[str] = mapped_column(String,nullable=False)
    content:Mapped[str] = mapped_column(String(255),nullable=False)