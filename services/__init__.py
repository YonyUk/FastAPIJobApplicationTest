from fastapi import Depends
from repositories import (
    get_post_repository,
    get_user_repository,
    get_comment_repository,
    get_tag_repository,
    UserRepository,
    PostRepository,
    CommentRepository,
    TagRepository
)
from .user import UserService
from .post import PostService
from .comment import CommentService
from .tag import TagService
from .authorization import AuthorizationService
from models import User
from security import get_current_user

def get_user_service(repository:UserRepository = Depends(get_user_repository)):
    '''
    gets the user service dependency
    '''
    service = UserService(repository)
    try:
        yield service
    finally:
        service = None

def get_post_service(
    post_repository:PostRepository = Depends(get_post_repository),
    tag_repository:TagRepository = Depends(get_tag_repository),
    comment_repository:CommentRepository = Depends(get_comment_repository),
    user_repository:UserRepository = Depends(get_user_repository)
):
    '''
    gets the post service dependency
    '''
    service = PostService(
        post_repository,
        tag_repository,
        comment_repository,
        user_repository
    )
    try:
        yield service
    finally:
        service = None

def get_comment_service(repository:CommentRepository=Depends(get_comment_repository)):
    '''
    gets the comment service dependency
    '''
    service = CommentService(repository)
    try:
        yield service
    finally:
        service = None

def get_tag_service(repository:TagRepository=Depends(get_tag_repository)):
    '''
    gets the tag service dependency
    '''
    service = TagService(repository)
    try:
        yield service
    finally:
        service = None

def get_authorization_service(user:User=Depends(get_current_user)):
    service = AuthorizationService(user)
    try:
        yield service
    finally:
        service = None