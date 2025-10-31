from typing import Sequence
from repositories import PostRepository,TagRepository,CommentRepository,UserRepository
from models import Post,Tag,Comment,User
from schemas import (
    PostCreateSchema,
    PostUpdateSchema,
    PostSchema,
    PostTagNestedSchema,
    PostCommentNestedSchema
)

class PostService:

    def __init__(
        self,post_repository:PostRepository,
        tag_repository:TagRepository,
        comment_repository:CommentRepository,
        user_repository:UserRepository
    ):
        '''
        service for the 'Post' entity
        '''
        self._post_repository = post_repository
        self._tag_repository = tag_repository
        self._comment_repository = comment_repository
        self._user_repository = user_repository

    def _get_post_instance(
        self,author_id:str,
        post:PostCreateSchema | PostUpdateSchema,
        post_id:str | None = None
    ) -> Post:
        data = post.model_dump(exclude={'tags'},exclude_unset=True)
        post_instance = Post(**data,author_id=author_id)

        if post_id:
            post_instance.id = post_id
        
        return post_instance
    
    async def _comments_to_schema(
        self,
        comments:Sequence[Comment]
    ) -> Sequence[PostCommentNestedSchema]:
        result = []
        for comment in comments:
            author = await self._user_repository.get_by_id(comment.author_id)
            result.append(
                PostCommentNestedSchema(
                    author=author.username, # type: ignore
                    content=comment.content
                )
            )
        return result
    
    async def _tags_to_schemas(
        self,
        tags:Sequence[Tag]
    ) -> Sequence[PostTagNestedSchema]:
        result = []
        for tag in tags:
            result.append(
                PostTagNestedSchema(
                    name=tag.name,
                    description=tag.description
                )
            )
        return result
    
    async def _post_to_schema(self,post:Post) -> PostSchema:
        comments = await self._comments_to_schema(post.comments)
        tags = await self._tags_to_schemas(post.tags)
        return PostSchema(
            created_at=post.created_at,
            updated_at=post.updated_at,
            title=post.title,
            content=post.content,
            tags=tags,
            comments=comments,
            id=post.id,
            author_id=post.author_id
        )
    
    async def _process_tags(self,tags:Sequence[PostTagNestedSchema]) -> Sequence[Tag]:
        result = []
        for tag in tags:
            db_tag = await self._tag_repository.get_by_name(tag.name)
            if db_tag is None:
                tag_model = Tag(**tag.model_dump())
                db_tag = await self._tag_repository.create(tag_model)
            result.append(db_tag)
        return result

    async def get_by_id(self,post_id:str) -> PostSchema | None:
        '''
        gets a post by it's id
        '''
        result = await self._post_repository.get_by_id(post_id)
        if result is None:
            return None
        return await self._post_to_schema(result)
    
    async def get_by_title(self,post_title:str) -> PostSchema | None:
        '''
        gets a post by it's title
        '''
        result = await self._post_repository.get_by_title(post_title)
        if result is None:
            return None
        return await self._post_to_schema(result)
    
    async def get_all(self,limit:int=100,skip:int=0) -> Sequence[PostSchema]:
        '''
        gets all the posts

        params:
            limit:int -> limit of results by response
            skip:int -> number of registers to skip
        '''
        db_posts = await self._post_repository.get_all(limit,skip)
        result = []
        for post in db_posts:
            r_post = await self._post_to_schema(post)
            result.append(r_post)
        return result
    
    async def create(self,author_id:str,post:PostCreateSchema) -> PostSchema | None:
        '''
        creates a post
        '''
        db_post = self._get_post_instance(author_id,post)

        if post.tags:
            db_post.tags = await self._process_tags(post.tags)
        result = await self._post_repository.create(db_post)
        if result is None:
            return None
        return await self._post_to_schema(result)
    
    async def update(self,post_id:str,post_update:PostUpdateSchema) -> PostSchema | None:
        '''
        update a post
        '''
        post = await self._post_repository.get_by_id(post_id)
        if post is None:
            return None
        db_post = self._get_post_instance(post.author_id,post_update,post_id)
        if post_update.tags:
            db_post.tags = await self._process_tags(post_update.tags)
        db_post.created_at = post.created_at
        db_post.updated_at = post.updated_at
        result = await self._post_repository.update(post_id,db_post)
        if result is None:
            return None
        return await self._post_to_schema(result)
    
    async def delete(self,post_id:str) -> bool:
        '''
        deletes a post
        '''
        return await self._post_repository.delete(post_id)