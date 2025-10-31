from typing import List
from repositories import PostRepository
from models import Post
from schemas import PostCreateSchema,PostUpdateSchema

class PostService:

    def __init__(self,repository:PostRepository):
        '''
        service for the 'Post' entity
        '''
        self._repository = repository

    def _get_post_instance(self,author_name:str,post:PostCreateSchema | PostUpdateSchema,post_id:str | None = None) -> Post:
        post = Post(
            id=post_id,
            title=post.title,
            content=post.content,
            author_name=author_name
        )
        return post

    async def get_by_id(self,post_id:str) -> Post | None:
        '''
        gets a post by it's id
        '''
        return await self._repository.get_by_id(post_id)
    
    async def get_by_title(self,post_title:str) -> Post | None:
        '''
        gets a post by it's title
        '''
        return await self._repository.get_by_title(post_title)
    
    async def get_all(self,limit:int=100,skip:int=0) -> List[Post]:
        '''
        gets all the posts

        params:
            limit:int -> limit of results by response
            skip:int -> number of registers to skip
        '''
        return await self._repository.get_all(limit,skip)

    async def create(self,author_name:str,post:PostCreateSchema) -> Post | None:
        '''
        creates a post
        '''
        db_post = self._get_post_instance(author_name,post)
        return await self._repository.create(db_post)
    
    async def update(self,post_id:str,author_name:str,post_update:PostUpdateSchema) -> Post | None:
        '''
        update a post
        '''
        db_post = self._get_post_instance(author_name,post_update,post_id)
        return await self._repository.update(post_id,db_post)
    
    async def delete(self,post_id:str) -> bool:
        '''
        deletes a post
        '''
        return await self._repository.delete(post_id)