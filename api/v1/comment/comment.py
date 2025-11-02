from typing import Sequence
from fastapi import APIRouter,HTTPException,status,Depends,Query
from models import User
from schemas import CommentCreateSchema,CommentUpdateSchema,CommentSchema
from security import get_current_user,get_authorization_service
from services import (
    CommentService,
    PostService,
    AuthorizationService,
    get_comment_service,
    get_post_service
)
from settings import ENVIRONMENT

router = APIRouter(prefix='/comments',tags=['comments'])

@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=CommentSchema
)
async def post_comment(
    post_id:str,
    comment:CommentCreateSchema,
    comment_service:CommentService=Depends(get_comment_service),
    post_service:PostService=Depends(get_post_service),
    current_user:User=Depends(get_current_user)
):
    db_post = await post_service.get_by_id(post_id)
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Not post with id "{post_id}" found'
        )
    db_comment = await comment_service.create(comment,author_id=current_user.id,post_id=post_id)
    if db_comment is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='An unexpected error has ocurred'
        )
    return db_comment

@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=Sequence[CommentSchema]
)
async def get_comments(
    page:int=Query(0,ge=0,description='page of results'),
    include_deleted:bool=Query(False,description='include deleted items'),
    service:CommentService=Depends(get_comment_service)
):
    return await service.get_all(
        ENVIRONMENT.PAGES_SIZE,
        page*ENVIRONMENT.PAGES_SIZE,
        include_deleted
    )

@router.get(
    '/{comment_id}',
    status_code=status.HTTP_200_OK,
    response_model=CommentSchema
)
async def get_by_id(
    comment_id:str,
    include_deleted:bool=Query(False,description='include deleted items'),
    service:CommentService=Depends(get_comment_service)
):
    db_comment = await service.get_by_id(comment_id,include_deleted)
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
    service:CommentService=Depends(get_comment_service),
    authorization_service:AuthorizationService=Depends(get_authorization_service)
):
    db_comment = await service.get_by_id(comment_id)
    if db_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not comment with id "{comment_id}" found'
        )
    if not authorization_service.validate_modification(db_comment.author_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
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
    service:CommentService=Depends(get_comment_service),
    authorization_service:AuthorizationService=Depends(get_authorization_service)
):
    db_comment = await service.get_by_id(comment_id)
    if db_comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not comment with id "{comment_id}" found'
        )
    
    if not authorization_service.validate_deletion(db_comment.author_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Only can modify comments of your own'
        )
    
    result = await service.delete(comment_id)
    return {'messsage':'comment deleted' if result else 'comment was not deleted'}