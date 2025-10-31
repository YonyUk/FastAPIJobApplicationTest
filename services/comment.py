from typing import Sequence
from repositories import CommentRepository
from models import Comment
from schemas import CommentCreateSchema,CommentUpdateSchema,CommentSchema

class CommentService:

    def __init__(self,repository:CommentRepository):
        '''
        service for 'Comment' entity
        '''
        self._repository = repository
    
    def _get_comment_instance(
            self,author_id:str,post_id:str,
            comment:CommentCreateSchema | CommentUpdateSchema,
            comment_id:str | None = None
    ) -> Comment:
        return Comment(
            id=comment_id,
            author_id=author_id,
            content=comment.content,
            post_id=post_id
        )
    
    async def get_by_id(self,comment_id:str) -> CommentSchema | None:
        '''
        gets a comment by its id
        '''
        return await self._repository.get_by_id(comment_id)
    
    async def get_all(self,limit:int=100,skip:int=0) -> Sequence[Comment]:
        '''
        gets all the comments

        params:
            limit:int -> limit of results by response
            skip:int -> number of registers to skip
        '''
        return await self._repository.get_all(limit,skip)
    
    async def create(self,author_id:str,post_id:str,comment:CommentCreateSchema) -> CommentSchema | None:
        '''
        creates a new comment
        '''
        db_comment = self._get_comment_instance(author_id,post_id,comment)
        return await self._repository.create(db_comment)
    
    async def update(self,comment_id:str,comment_update:CommentUpdateSchema) -> CommentSchema | None:
        '''
        updates a comment
        '''
        comment = await self._repository.get_by_id(comment_id)
        if comment is None:
            return None
        db_comment = self._get_comment_instance(comment.author_id,comment.post_id,comment_update,comment_id)
        db_comment.created_at = comment.created_at
        db_comment.updated_at = comment.updated_at
        return await self._repository.update(db_comment.id,db_comment)
    
    async def delete(self,comment_id:str) -> bool:
        '''
        deletes a comment
        '''
        return await self._repository.delete(comment_id)