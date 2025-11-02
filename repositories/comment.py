from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Comment
from .base import BaseRepository

class CommentRepository(BaseRepository):

    def __init__(self,db:AsyncSession):
        '''
        repository for 'Comment' entity
        '''
        super().__init__(Comment,db)
    
    async def _get_instance_ignore_deleted(self, instance: Comment) -> Comment | None:
        return await self.get_by_id(instance.id)