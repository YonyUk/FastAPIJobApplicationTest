from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column
from uuid import uuid4
from database import BaseModel
from .mixins import TimestampMixin,SoftDeleteMixin

class Post(BaseModel,TimestampMixin,SoftDeleteMixin):
    '''
    Represent a 'post' entity in the database
    '''

    __tablename__ = 'posts'

    id:Mapped[str] = mapped_column(String,primary_key=True,default=lambda:str(uuid4()))
    title:Mapped[str] = mapped_column(String,unique=True,nullable=False,index=True)
    content:Mapped[str] = mapped_column(String,nullable=False)
    author_name:Mapped[str] = mapped_column(String,nullable=False)