from typing import Sequence
from fastapi import APIRouter,HTTPException,status,Depends
from models import User
from schemas import CommentCreateSchema,CommentUpdateSchema,CommentSchema
from security import get_current_user
from services import CommentService,get_comment_service

router = APIRouter(prefix='/comments',tags=['comments'])

@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=CommentSchema
)
async def post_comment(
    post_id:str,
    comment:CommentCreateSchema,
    service:CommentService=Depends(get_comment_service),
    current_user:User=Depends(get_current_user)
):
    return await service.create(current_user.id,post_id,comment)