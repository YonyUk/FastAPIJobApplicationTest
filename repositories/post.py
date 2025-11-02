from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update
from models import Post
from .base import BaseRepository

class PostRepository(BaseRepository):

    def __init__(self,db:AsyncSession):
        '''
        database repository for 'Post' entity
        '''
        super().__init__(Post,db)
    
    async def _get_instance_ignore_deleted(self, instance: Post) -> Post | None:
        if not instance.id is None:
            return await self.get_by_id(instance.id,True)
        return await self.get_by_title(instance.title,True)
    
    async def get_by_title(self,post_title:str,include_deleted:bool=False) -> Post | None:
        '''
        gets a post by its title
        '''
        query = select(Post)
        if include_deleted:
            query = query.where(Post.title==post_title)
        else:
            query = query.where((Post.title==post_title) & (Post.is_deleted != True))
        result = await self._db.execute(query)
        return result.scalar_one_or_none()
    
    async def update(self, instance_id: str, update_instance: Post) -> Post | None:
        db_instance = await self.get_by_id(instance_id)
        if db_instance is None:
            return None
        
        update_instance.created_at = db_instance.created_at
        update_instance.updated_at = db_instance.updated_at
        update_data = self._instance_to_dict(update_instance)
        await self._db.execute(
            update(self._model).where((self._model.is_deleted != True) & (self._model.id==instance_id)).values(**update_data)
        )
        if update_instance.tags:
            db_instance.tags = update_instance.tags
        await self._db.commit()
        await self._db.refresh(db_instance)
        
        return db_instance