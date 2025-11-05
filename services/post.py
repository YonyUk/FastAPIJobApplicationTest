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
    ):
        '''
        service for 'Post'
        '''
        super().__init__(Post,post_repository,{'tags'},True)
        self._tag_repository = tag_repository
    
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
    
    def _comments_to_schema(
        self,
        comments:Sequence[Comment]
    ) -> Sequence[PostCommentNestedSchema]:
        comments_ = filter(lambda comment:not comment.is_deleted,comments)
        return list(map(
            lambda comment:PostCommentNestedSchema(
                author=comment.author.username
                ,content=comment.content
                ),
            comments_
        ))

    def _tags_to_schemas(
        self,
        tags:Sequence[Tag]
    ) -> Sequence[PostTagNestedSchema]:
        tags_ = filter(lambda tag:not tag.is_deleted,tags)
        return list(map(
            lambda tag:PostTagNestedSchema(
                name=tag.name,
                description=tag.description
            ),
            tags_
        ))
    
    async def _to_schema(self,model:Post) -> PostSchema:
        return PostSchema(
            created_at=model.created_at,
            updated_at=model.updated_at,
            title=model.title,
            content=model.content,
            tags=self._tags_to_schemas(model.tags),
            comments=self._comments_to_schema(model.comments),
            id=model.id,
            author_id=model.author_id
        )
    
    async def get_by_title(self,post_title:str,include_deleted:bool=False) -> PostSchema | None:
        '''
        gets a post by its title
        '''
        result = await self._repository.get_by_title(post_title,include_deleted)
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