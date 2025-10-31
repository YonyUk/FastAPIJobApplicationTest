from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update
from models import Tag

class TagRepository:

    def __init__(self,db:AsyncSession):
        '''
        repository for 'Tag' entity
        '''
        self._db = db
    
    def _tag_to_dict(self,tag: Tag) -> dict:
        return {
            'id':tag.id,
            'name':tag.name,
            'description':tag.description,
            'created_at':tag.created_at,
            'updated_at':tag.updated_at,
            'is_deleted':tag.is_deleted,
            'deleted_at':tag.deleted_at
        }
    
    async def get_tag_ignore_deleted(self,tag:Tag) -> Tag | None:
        '''
        gets a tag by any of its unique fields ignoring if it was deleted
        '''
        result = None
        if not tag.id is None:
            result = await self._db.execute(
                select(Tag).where(Tag.id==tag.id)
            )
        else:
            result = await self._db.execute(
                select(Tag).where(Tag.name==tag.name)
            )
        return result.scalar_one_or_none()
    
    async def get_by_id(self,tag_id:str) -> Tag | None:
        '''
        gets a tag by its id
        '''
        result = await self._db.execute(
            select(Tag).where((Tag.is_deleted != True) & (Tag.id==tag_id))
        )
        return result.scalar_one_or_none()
    
    async def get_all(self,limit:int=100,skip:int=0) -> Sequence[Tag]:
        '''
        gets all the tags

        params:
            limit:int -> limit of results by response
            skip:int -> number of registers to skip
        '''
        result = await self._db.execute(
            select(Tag).where(Tag.is_deleted != True).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def create(self,tag:Tag) -> Tag | None:
        '''
        creates a tag
        '''
        db_tag = await self.get_tag_ignore_deleted(tag)
        if db_tag is None:
            self._db.add(tag)
            await self._db.commit()
            await self._db.refresh(db_tag)
            return db_tag
        elif db_tag.is_deleted:
            db_tag.restore()
            update_data = self._tag_to_dict(tag)
            await self._db.execute(
                update(Tag).where(Tag.id==db_tag.id).values(**update_data)
            )
            await self._db.commit()
            await self._db.refresh(db_tag)
            return db_tag
        else:
            return None
    
    async def update(self,tag_id:str,tag_update:Tag) -> Tag | None:
        '''
        updates a tag
        '''
        db_tag = await self.get_by_id(tag_id)
        if db_tag is None:
            return None
        
        tag_update.created_at = db_tag.created_at
        tag_update.updated_at = db_tag.updated_at
        update_data = self._tag_to_dict(tag_update)
        await self._db.execute(
            update(Tag).where((Tag.is_deleted != True) & (Tag.id==tag_id)).values(**update_data)
        )
        await self._db.commit()
        await self._db.refresh(db_tag)
        
        return db_tag
    
    async def delete(self,tag_id:str) -> bool:
        '''
        deletes a tag
        '''
        db_tag = await self.get_by_id(tag_id)
        if db_tag is None:
            return False
        
        db_tag.soft_delete()
        await self._db.commit()
        await self._db.refresh(db_tag)
        
        return True