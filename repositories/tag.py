from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update
from models import Tag
from .base import BaseRepository

class TagRepository(BaseRepository[Tag]):

    def __init__(self,db:AsyncSession):
        '''
        repository for 'Tag'
        '''
        super().__init__(Tag,db)
    
    async def _get_instance_ignore_deleted(self, instance: Tag) -> Tag | None:
        db_tag = await self.get_by_id(instance.id,True)
        if not db_tag is None:
            return db_tag
        return await self.get_by_name(instance.name,True)

    async def get_by_name(self,tag_name:str,include_deleted:bool=False) -> Tag | None:
        '''
        gets a tag by its name
        '''
        result = await self._db.execute(
            select(Tag).where(Tag.name==tag_name)
        )
        if include_deleted:
            return result.scalar_one_or_none()
        tag = result.scalar_one_or_none()
        if not tag is None and tag.is_deleted and not include_deleted:
            return None
        return tag