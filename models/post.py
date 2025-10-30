from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column
from uuid import uuid4
from database import BaseModel

class Post(BaseModel):
    '''
    Represent a 'post' entity in the database
    '''

    __tablename__ = 'posts'

    id:Mapped[str] = mapped_column(String,primary_key=True,default=lambda:str(uuid4()))
    title:Mapped[str] = mapped_column(String,unique=True,nullable=False,index=True)
    content:Mapped[str] = mapped_column(String,nullable=False)