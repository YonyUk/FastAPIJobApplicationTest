from sqlalchemy import String,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship
from uuid import uuid4
from database import BaseModel
from .mixins import TimestampMixin,SoftDeleteMixin

class Comment(BaseModel,TimestampMixin,SoftDeleteMixin):
    '''
    comment entity
    '''
    __tablename__ = 'comments'

    id:Mapped[str] = mapped_column(String,primary_key=True,default=lambda:str(uuid4()))
    content:Mapped[str] = mapped_column(String(255),nullable=False)
    author_id:Mapped[str] = mapped_column(String,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    post_id:Mapped[str] = mapped_column(String,ForeignKey('posts.id',ondelete='CASCADE'),nullable=False)

    author = relationship('User',back_populates='comments')

    post = relationship('Post',back_populates='comments')