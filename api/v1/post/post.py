from typing import Sequence
from fastapi import APIRouter,HTTPException,status,Depends,Query
from models import User
from schemas import PostCreateSchema,PostUpdateSchema,PostSchema
from security import get_current_user
from services import PostService,get_post_service,AuthorizationService,get_authorization_service
from settings import ENVIRONMENT

router = APIRouter(prefix='/posts',tags=['posts'])

@router.post(
    '/create',
    response_model=PostSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    post:PostCreateSchema,
    service:PostService=Depends(get_post_service),
    current_user:User=Depends(get_current_user)
):
    db_post = await service.get_by_title(post.title)
    if not db_post is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'A post with title "{post.title}" already exists'
        )
    return await service.create(post,author_id=current_user.id)

@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=Sequence[PostSchema]
)
async def get_posts(
    page:int=Query(0,ge=0,description='page of results'),
    include_deleted:bool=Query(False,description='include deleted items'),
    service:PostService=Depends(get_post_service)
):
    return await service.get_all(
        ENVIRONMENT.PAGES_SIZE,
        page*ENVIRONMENT.PAGES_SIZE,
        include_deleted
    )

@router.get(
    '/{post_id}',
    status_code=status.HTTP_200_OK,
    response_model=PostSchema
)
async def get_by_id(
    post_id:str,
    include_deleted:bool=Query(False,description='include deleted items'),
    service:PostService=Depends(get_post_service)
):
    db_post = await service.get_by_id(post_id,include_deleted)
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not post with id "{post_id}" found'
        )
    return db_post

@router.get(
    '/title/{post_title}',
    status_code=status.HTTP_200_OK,
    response_model=PostSchema
)
async def get_by_title(
    post_title:str,
    include_deleted:bool=Query(False,description='include deleted items'),
    service:PostService=Depends(get_post_service)
):
    db_post = await service.get_by_title(post_title,include_deleted)
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not post with title "{post_title}" found'
        )
    return db_post

@router.put(
    '/{post_id}',
    response_model=PostSchema,
    status_code=status.HTTP_202_ACCEPTED
)
async def update_post(
    post_id:str,
    post_update:PostUpdateSchema,
    current_user:User=Depends(get_current_user),
    service:PostService=Depends(get_post_service),
    authorization_service:AuthorizationService=Depends(get_authorization_service)
):
    db_post = await service.get_by_id(post_id)
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not post with id "{post_id}" found'
        )
    if not authorization_service.validate_modification(post_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only can modify posts of your own'
        )
    db_post = await service.update(post_id,post_update,author_id=current_user.id)
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Something went wrong in the server'
        )
    return db_post

@router.delete(
    '/{post_id}',
    status_code=status.HTTP_202_ACCEPTED
)
async def delete(
    post_id:str,
    service:PostService=Depends(get_post_service),
    authorization_service:AuthorizationService=Depends(get_authorization_service)
):
    db_post = await service.get_by_id(post_id)
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not post with id "{post_id}" found'
        )
    if not authorization_service.validate_deletion(post_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only can delete posts of your own'
        )
    result = await service.delete(post_id)
    return {'messsage':'post deleted' if result else 'post was not deleted'}