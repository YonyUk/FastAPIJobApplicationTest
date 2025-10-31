from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column,relationship
from uuid import uuid4
from database import BaseModel
from .mixins import TimestampMixin,SoftDeleteMixin

class User(BaseModel,TimestampMixin,SoftDeleteMixin):
    '''
    Represents an 'user' entity in the database
    '''
    __tablename__ = 'users'

    id:Mapped[str] = mapped_column(String,primary_key=True,default=lambda:str(uuid4()))
    username:Mapped[str] = mapped_column(String,unique=True,nullable=False,index=True)
    email:Mapped[str] = mapped_column(String,unique=True,index=True,nullable=False)
    hashed_password:Mapped[str] = mapped_column(String,nullable=False)

    posts = relationship('Post',back_populates='author',cascade='all, delete-orphan')

    comments = relationship('Comment',back_populates='author',cascade='all, delete-orphan')