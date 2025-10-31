from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update
from models import Post

class PostRepository:

    def __init__(self,db:AsyncSession):
        '''
        database repository for 'Post' entity
        '''
        self._db = db
    
    def _post_to_dict(self,post:Post) -> dict:
        return {
            'id':post.id,
            'title':post.title,
            'content':post.content,
            'created_at':post.created_at,
            'updated_at':post.updated_at,
            'is_deleted':post.is_deleted if not post.is_deleted is None else False,
            'deleted_at':post.deleted_at
        }
    
    async def get_post_ignore_deleted(self,post:Post) -> Post | None:
        '''
        gets a post bay any of its unique fields ignoring if it was deleted
        '''
        result = None
        if not post.id is None:
            result = await self._db.execute(
                select(Post).where(Post.id==post.id)
            )
        else:
            result = await self._db.execute(
                select(Post).where(Post.title==post.title)
            )
        return result.scalar_one_or_none()
    
    async def get_by_id_ignore_deleted(self,post_id:str) -> Post | None:
        '''
        gets a post by its id ignoring if it was deleted
        '''
        result = await self._db.execute(
            select(Post).where(Post.id==post_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_title_ignore_deleted(self,post_title:str) -> Post | None:
        '''
        gets a post by its title ignoring if it was deleted
        '''
        result = await self._db.execute(
            select(Post).where(Post.title==post_title)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self,post_id:str) -> Post | None:
        '''
        gets a post by it's id
        '''
        result = await self._db.execute(
            select(Post).where((Post.id==post_id) & (Post.is_deleted != True))
        )
        return result.scalar_one_or_none()
    
    async def get_by_title(self,post_title:str) -> Post | None:
        '''
        gets a post by it's title
        '''
        result = await self._db.execute(
            select(Post).where((Post.title==post_title) & (Post.is_deleted != True))
        )
        return result.scalar_one_or_none()

    async def get_all(self,limit:int=100,skip:int=0) -> List[Post]:
        '''
        gets all the posts

        params:

            limit:int -> limit of results by response
            skip:int -> number of registers to skip
        '''
        result = await self._db.execute(
            select(Post).where(Post.is_deleted != True).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self,post:Post) -> Post | None:
        '''
        creates a new 'Post' in the database

        returns None if the post wasn't created
        '''
        db_post = await self.get_post_ignore_deleted(post)
        if not db_post:
            self._db.add(post)
            await self._db.commit()
            await self._db.refresh(post)
            return post
        elif db_post.is_deleted:
            db_post.restore()
            update_data = self._post_to_dict(db_post)
            await self._db.execute(
                update(Post).where(Post.id==db_post.id).values(**update_data)
            )
            await self._db.commit()
            await self._db.refresh(db_post)
            return db_post
        else:
            return None
    
    async def update(self,post_id:str,post_update:Post) -> Post | None:
        '''
        updates a 'Post' in the database
        '''
        update_data = self._post_to_dict(post_update)
        db_post = await self.get_by_id(post_id)
        await self._db.execute(
            update(Post).where((Post.id==post_id) & (Post.is_deleted != True)).values(**update_data)
        )
        await self._db.commit()
        await self._db.refresh(db_post)
        
        return db_post
    
    async def delete(self,post_id:str) -> bool:
        '''
        deletes a post
        '''
        db_post = await self.get_by_id(post_id)
        if db_post is None:
            return False
        
        db_post.soft_delete()
        await self._db.commit()
        await self._db.refresh(db_post)
        return True