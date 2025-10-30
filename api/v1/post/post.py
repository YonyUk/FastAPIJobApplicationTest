from fastapi import APIRouter,HTTPException,status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from models import Post,User
from schemas import PostCreateSchema,PostUpdateSchema,PostSchema
from security import create_access_token,get_current_user
from settings import ENVIRONMENT
from services import PostService,get_post_service

router = APIRouter(prefix='/posts',tags=['posts'])

@router.post(
    '/create',
    response_model=PostSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    post:PostCreateSchema,
    status_code=status.HTTP_201_CREATED,
    service:PostService=Depends(get_post_service),
    current_user:User=Depends(get_current_user)
):
    db_post = await service.get_by_title(post.title)
    if not db_post is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'A post with title "{post.title}" already exists'
        )
    return await service.create(post)