from typing import Sequence
from repositories import TagRepository
from models import Tag
from schemas import TagCreateSchema,TagUpdateSchema,TagSchema

class TagService:

    def __init__(self,repository:TagRepository):
        '''
        service for 'Tag' entity
        '''
        self._repository = repository
    
    def _get_tag_instance(
        self,
        tag:TagCreateSchema | TagUpdateSchema,
        tag_id:str | None = None
    ) -> Tag:
        return Tag(**tag.model_dump(),id=tag_id)
    
    async def get_by_id(self,tag_id:str) -> TagSchema | None:
        '''
        gets a tag by its id
        '''
        return await self._repository.get_by_id(tag_id)
    
    async def get_by_name(self,tag_name:str) -> TagSchema | None:
        '''
        gets a tag by its name
        '''
        return await self._repository.get_by_name(tag_name)
    
    async def get_all(self,limit:int=100,skip:int=0) -> Sequence[TagSchema]:
        '''
        gets all the tags

        params:
            limit:int -> limit of results by response
            skip:int -> number of registers to skip
        '''
        return await self._repository.get_all(limit,skip)
    
    async def create(self,tag:TagCreateSchema) -> TagSchema | None:
        '''
        creates a tag
        '''
        db_tag = self._get_tag_instance(tag)
        return await self._repository.create(db_tag)
    
    async def update(self,tag_id:str,tag_update:TagUpdateSchema) -> TagSchema | None:
        '''
        updates a tag
        '''
        tag = await self._repository.get_by_id(tag_id)
        if tag is None:
            return None
        
        db_tag = self._get_tag_instance(tag_update,tag_id)
        db_tag.created_at = tag.created_at
        db_tag.updated_at = tag.updated_at
        db_tag.is_deleted = tag.is_deleted
        return await self._repository.update(tag_id,db_tag)
    
    async def delete(self,tag_id:str) -> bool:
        '''
        deletes a tag
        '''
        return await self._repository.delete(tag_id)