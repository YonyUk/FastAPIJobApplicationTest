from repositories import PostRepository
from models import Post
from schemas import PostCreateSchema,PostUpdateSchema

class PostService:

    def __init__(self,repository:PostRepository):
        '''
        service for the 'Post' entity
        '''
        self._repository = repository

    def _get_post_instance(self,post:PostCreateSchema | PostUpdateSchema,post_id:str | None = None) -> Post:
        post = Post(
            id=post_id,
            title=post.title,
            content=post.content,
            author_name=post.author_name
        )
        return post

    async def get_by_id(self,post_id:str) -> Post:
        '''
        gets a post by it's id
        '''
        return await self._repository.get_by_id(post_id)
    
    async def get_by_title(self,post_title:str) -> Post:
        '''
        gets a post by it's title
        '''
        return await self._repository.get_by_title(post_title)

    async def create(self,post:PostCreateSchema) -> Post:
        '''
        creates a post
        '''
        db_post = self._get_post_instance(post)
        return await self._repository.create(db_post)
    
    async def update(self,post_id:str,post_update:PostUpdateSchema) -> Post:
        '''
        update a post
        '''
        db_post = self._get_post_instance(post_update,post_id)
        return await self._repository.update(post_id,db_post)
    
    async def delete(self,post_id:str) -> bool:
        '''
        deletes a post
        '''
        return await self._repository.delete(post_id)