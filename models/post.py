from sqlalchemy import Column, String,ForeignKey,Table
from sqlalchemy.orm import Mapped,mapped_column,relationship
from uuid import uuid4
from database import BaseModel
from .mixins import TimestampMixin,SoftDeleteMixin

posts_tags = Table(
    'posts_tags',
    BaseModel.metadata,
    Column('post_id',String,ForeignKey('posts.id',ondelete='CASCADE'),primary_key=True),
    Column('tag_id',String,ForeignKey('tags.id',ondelete='CASCADE'),primary_key=True)
)

class Post(BaseModel,TimestampMixin,SoftDeleteMixin):
    '''
    Represent a 'post' entity in the database
    '''

    __tablename__ = 'posts'

    id:Mapped[str] = mapped_column(String,primary_key=True,default=lambda:str(uuid4()))
    title:Mapped[str] = mapped_column(String,unique=True,nullable=False,index=True)
    content:Mapped[str] = mapped_column(String,nullable=False)
    author_id:Mapped[str] = mapped_column(String,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)

    author = relationship('User',back_populates='posts',lazy='joined')

    comments = relationship('Comment',back_populates='post',cascade='all, delete-orphan',lazy='selectin')

    tags = relationship('Tag',back_populates='posts',secondary=posts_tags,lazy='selectin')