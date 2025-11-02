from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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