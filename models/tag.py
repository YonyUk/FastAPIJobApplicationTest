from sqlalchemy import ForeignKey,String
from sqlalchemy.orm import Mapped,mapped_column,relationship
from uuid import uuid4
from database import BaseModel
from .mixins import TimestampMixin,SoftDeleteMixin

class Tag(BaseModel,TimestampMixin,SoftDeleteMixin):

    __tablename__ = 'tags'

    id:Mapped[str] = mapped_column(String,primary_key=True,default=lambda:str(uuid4()))
    name:Mapped[str] = mapped_column(String,unique=True,index=True,nullable=False)
    description:Mapped[str] = mapped_column(String(255),nullable=True)

    posts = relationship('Post',back_populates='tags',secondary='posts_tags',lazy='selectin')