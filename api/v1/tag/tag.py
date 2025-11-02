from typing import Sequence
from fastapi import APIRouter,HTTPException,status,Depends
from models import User
from schemas import TagCreateSchema,TagUpdateSchema,TagSchema
from security import get_current_user
from services import TagService,get_tag_service

router = APIRouter(prefix='/tags',tags=['tags'])

@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=TagSchema
)
async def post_tag(
    tag:TagCreateSchema,
    current_user:User=Depends(get_current_user),
    service:TagService=Depends(get_tag_service)
):
    db_tag = await service.get_by_name(tag.name)
    if not db_tag is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'A tag named "{tag.name}" already exists'
        )
    return await service.create(tag)

@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=Sequence[TagSchema]
)
async def get_tags(
    service:TagService=Depends(get_tag_service)
):
    return await service.get_all()

@router.get(
    '/{tag_id}',
    status_code=status.HTTP_200_OK,
    response_model=TagSchema
)
async def get_by_id(
    tag_id:str,
    service:TagService=Depends(get_tag_service)
):
    db_tag = await service.get_by_id(tag_id)
    if db_tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not tag with id "{tag_id}" found'
        )
    return db_tag

@router.get(
    '/name/{tag_name}',
    status_code=status.HTTP_200_OK,
    response_model=TagSchema
)
async def get_by_name(
    tag_name:str,
    service:TagService=Depends(get_tag_service)
):
    db_tag = await service.get_by_name(tag_name)
    if db_tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not tag with name "{tag_name}" found'
        )
    return db_tag

@router.put(
    '/{tag_id}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=TagSchema
)
async def update(
    tag_id:str,
    tag_update:TagUpdateSchema,
    current_user:User=Depends(get_current_user),
    service:TagService=Depends(get_tag_service)
):
    db_tag = await service.get_by_id(tag_id)
    if db_tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Not tag with id "{tag_id}" found'
        )
    db_tag = await service.update(tag_id,tag_update)
    if db_tag is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='An unexpected error has ocurred'
        )
    return db_tag

@router.delete(
    '/{tag_id}',
    status_code=status.HTTP_202_ACCEPTED
)
async def delete_tag(
    tag_id:str,
    current_user:User=Depends(get_current_user),
    service:TagService=Depends(get_tag_service)
):
    result = await service.delete(tag_id)
    return {'messsage':'tag deleted' if result else 'tag was not deleted'}