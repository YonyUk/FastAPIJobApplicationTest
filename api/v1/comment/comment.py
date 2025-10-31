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

@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=Sequence[CommentSchema]
)
async def get_comments(
    service:CommentService=Depends(get_comment_service)
):
    return await service.get_all()

@router.get(
    '/{comment_id}',
    status_code=status.HTTP_200_OK,
    response_model=CommentSchema
)
async def get_by_id(
    comment_id:str,
    service:CommentService=Depends(get_comment_service)
):
    db_comment = await service.get_by_id(comment_id)
    if db_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not comment with id "{comment_id}" found'
        )
    return db_comment

@router.put(
    '/{comment_id}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=CommentSchema
)
async def update_comment(
    comment_id:str,
    comment:CommentUpdateSchema,
    current_user:User=Depends(get_current_user),
    service:CommentService=Depends(get_comment_service)
):
    db_comment = await service.get_by_id(comment_id)
    if db_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not comment with id "{comment_id}" found'
        )
    if db_comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Only can modify comments of your own'
        )
    db_comment = await service.update(comment_id,comment)
    if db_comment is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='An unexpected error has ocurred'
        )
    return db_comment

@router.delete(
    '/{comment_id}',
    status_code=status.HTTP_202_ACCEPTED
)
async def delete_comment(
    comment_id:str,
    current_user:User=Depends(get_current_user),
    service:CommentService=Depends(get_comment_service)
):
    db_comment = await service.get_by_id(comment_id)
    if db_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not comment with id "{comment_id}" found'
        )
    
    if db_comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Only can modify comments of your own'
        )
    
    result = await service.delete(comment_id)
    return {'messsage':'comment deleted' if result else 'comment was not deleted'}