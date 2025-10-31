from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update
from models import Comment

class CommentRepository:

    def __init__(self,db:AsyncSession):
        '''
        repository for 'Comment' entity
        '''
        self._db = db
    
    def _comment_to_dict(self,comment:Comment) -> dict:
        return {
            'id':comment.id,
            'content':comment.content,
            'author_id':comment.author_id,
            'post_id':comment.post_id,
            'created_at':comment.created_at,
            'updated_at':comment.updated_at,
            'is_deleted':comment.is_deleted if comment.is_deleted is not None else False,
            'deleted_at':comment.deleted_at
        }
    
    async def get_comment_ignore_deleted(self,comment_id:str) -> Comment | None:
        '''
        gets a comment by its id ignoring if it was deleted
        '''
        result = await self._db.execute(
            select(Comment).where(Comment.id==comment_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_id(self,comment_id:str) -> Comment | None:
        '''
        gets a comment by its id
        '''
        result = await self._db.execute(
            select(Comment).where((Comment.id==comment_id) & (Comment.is_deleted != True))
        )
        return result.scalar_one_or_none()
    
    async def get_all(self,limit:int=100,skip:int=0) -> Sequence[Comment]:
        '''
        gets all the comments

        params:
            limit:int -> limit of results by response
            skip:int -> number of registers to skip
        '''
        result = await self._db.execute(
            select(Comment).where(Comment.is_deleted != True).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def create(self,comment:Comment) -> Comment | None:
        '''
        creates a comment in database
        '''
        db_comment = await self.get_comment_ignore_deleted(comment.id)
        if not db_comment:
            self._db.add(comment)
            await self._db.commit()
            await self._db.refresh(comment)
            return comment
        elif db_comment.is_deleted:
            db_comment.restore()
            update_data = self._comment_to_dict(db_comment)
            await self._db.execute(
                update(Comment).where(Comment.id==db_comment.id).values(**update_data)
            )
            await self._db.commit()
            await self._db.refresh(db_comment)
            return db_comment
        else:
            return None
    
    async def update(self,comment_id:str,comment_update:Comment) -> Comment | None:
        '''
        updates a comment
        '''
        db_comment = await self.get_by_id(comment_id)
        if not db_comment:
            return None
        
        comment_update.created_at = db_comment.created_at
        comment_update.updated_at = db_comment.updated_at
        update_data = self._comment_to_dict(comment_update)
        await self._db.execute(
            update(Comment).where((Comment.id==db_comment.id) & (Comment.is_deleted != True)).values(**update_data)
        )
        await self._db.commit()
        await self._db.refresh(db_comment)
        return db_comment
    
    async def delete(self,comment_id:str) -> bool:
        '''
        deletes a comment
        '''
        db_comment = await self.get_by_id(comment_id)
        if db_comment is None:
            return False
        
        db_comment.soft_delete()
        await self._db.commit()
        await self._db.refresh(db_comment)

        return True
