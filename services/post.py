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
from .base import BaseService

class PostService(
    BaseService[
        Post,
        PostCreateSchema,
        PostUpdateSchema,
        PostSchema,
        PostRepository
    ]
):
    
    def __init__(
        self,
        post_repository:PostRepository,
        tag_repository:TagRepository,
        comment_repository:CommentRepository,
        user_repository:UserRepository
    ):
        '''
        service for 'Post'
        '''
        super().__init__(Post,post_repository,{'tags'},True)
        self._tag_repository = tag_repository
        self._comment_repository = comment_repository
        self._user_repository = user_repository
    
    async def _process_tags(self,tags:Sequence[PostTagNestedSchema]) -> Sequence[Tag]:
        result = []
        for tag in tags:
            db_tag = await self._tag_repository.get_by_name(tag.name)
            if db_tag is None:
                tag_model = Tag(**tag.model_dump())
                db_tag = await self._tag_repository.create(tag_model)
            result.append(db_tag)
        return result

    async def _process_before_update_modifier(
        self,
        update_data: PostUpdateSchema,
        existing_model: Post,
        model: Post
    ) -> Post:
        if update_data.tags:
            model.tags = await self._process_tags(update_data.tags)
        model.created_at = existing_model.created_at
        model.updated_at = existing_model.updated_at
        model.is_deleted = existing_model.is_deleted
        return model
    
    async def _comments_to_schema(
        self,
        comments:Sequence[Comment]
    ) -> Sequence[PostCommentNestedSchema]:
        result = []
        for comment in comments:
            if comment.is_deleted: continue
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
    
    async def _to_schema(self,model:Post) -> PostSchema:
        comments = await self._comments_to_schema(model.comments)
        tags = await self._tags_to_schemas(model.tags)
        return PostSchema(
            created_at=model.created_at,
            updated_at=model.updated_at,
            title=model.title,
            content=model.content,
            tags=tags,
            comments=comments,
            id=model.id,
            author_id=model.author_id
        )
    
    async def get_by_title(self,post_title:str) -> PostSchema | None:
        '''
        gets a post by its title
        '''
        result = await self._repository.get_by_title(post_title)
        if result is None:
            return None
        return await self._to_schema(result)
    
    async def _process_before_create(
        self,
        instance: Post,
        create_value: PostCreateSchema
    ) -> Post:
        if create_value.tags:
            instance.tags = await self._process_tags(create_value.tags)
        return instance