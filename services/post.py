from typing import List, Sequence
from repositories import PostRepository
from models import Post
from schemas import PostCreateSchema,PostUpdateSchema,PostSchema

class PostService:

    def __init__(self,repository:PostRepository):
        '''
        service for the 'Post' entity
        '''
        self._repository = repository

    def _get_post_instance(
        self,author_name:str,
        post:PostCreateSchema | PostUpdateSchema,
        post_id:str | None = None
    ) -> Post:
        return Post(
            id=post_id,
            title=post.title,
            content=post.content,
            author_name=author_name
        )
        

    async def get_by_id(self,post_id:str) -> PostSchema | None:
        '''
        gets a post by it's id
        '''
        return await self._repository.get_by_id(post_id)
    
    async def get_by_title(self,post_title:str) -> PostSchema | None:
        '''
        gets a post by it's title
        '''
        return await self._repository.get_by_title(post_title)
    
    async def get_all(self,limit:int=100,skip:int=0) -> Sequence[PostSchema]:
        '''
        gets all the posts

        params:
            limit:int -> limit of results by response
            skip:int -> number of registers to skip
        '''
        return await self._repository.get_all(limit,skip)
    
    async def get_by_author_name(self,author_name:str,limit:int=100,skip:int=0) -> Sequence[PostSchema]:
        '''
        gets the posts by its author_name field

        params:
            limit:int -> limit of results by response
            skip:int -> number of registers to skip
        '''
        return await self._repository.get_by_author_name(author_name,limit,skip)

    async def create(self,author_name:str,post:PostCreateSchema) -> PostSchema | None:
        '''
        creates a post
        '''
        db_post = self._get_post_instance(author_name,post)
        return await self._repository.create(db_post)
    
    async def update(self,post_id:str,author_name:str,post_update:PostUpdateSchema) -> PostSchema | None:
        '''
        update a post
        '''
        post = await self._repository.get_by_id(post_id)
        if post is None:
            return None
        db_post = self._get_post_instance(author_name,post_update,post_id)
        db_post.created_at = post.created_at
        db_post.updated_at = post.updated_at
        return await self._repository.update(post_id,db_post)
    
    async def delete(self,post_id:str) -> bool:
        '''
        deletes a post
        '''
        return await self._repository.delete(post_id)