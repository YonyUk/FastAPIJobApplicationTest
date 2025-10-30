from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column
from uuid import uuid4
from database import BaseModel

class User(BaseModel):
    '''
    Represents an 'user' entity in the database
    '''
    __tablename__ = 'users'

    id:Mapped[str] = mapped_column(String,primary_key=True,default=lambda:str(uuid4()))
    username:Mapped[str] = mapped_column(String,unique=True,nullable=False,index=True)
    email:Mapped[str] = mapped_column(String,unique=True,index=True,nullable=False)
    hashed_password:Mapped[str] = mapped_column(String,nullable=False)