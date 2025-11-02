from typing import Sequence
from repositories import TagRepository
from models import Tag
from schemas import TagCreateSchema,TagUpdateSchema,TagSchema
from .base import BaseService

class TagService(
        BaseService[
            Tag,
            TagCreateSchema,
            TagUpdateSchema,
            TagSchema,
            TagRepository    
        ]
    ):

    def __init__(self,repository:TagRepository):
        '''
        service for 'Tag'
        '''
        super().__init__(Tag,repository)
    
    async def _process_before_update_modifier(
        self,
        update_data: TagUpdateSchema,
        existing_model: Tag,
        model: Tag
    ) -> Tag:
        model.created_at = existing_model.created_at
        model.updated_at = existing_model.updated_at
        model.is_deleted = existing_model.is_deleted
        return model
    
    async def get_by_name(self,tag_name:str) -> TagSchema:
        '''
        gets a tag by its name
        '''
        return await self._repository.get_by_name(tag_name)