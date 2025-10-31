from sqlalchemy import String,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship
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
    author_id:Mapped[str] = mapped_column(String,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)

    # ManyToOne: A comment have only one author
    author = relationship('User',back_populates='posts')