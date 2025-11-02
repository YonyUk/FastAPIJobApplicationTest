from typing import Generic, Sequence, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update
from database import BaseModel

ModelType = TypeVar('ModelType',bound=BaseModel) # type: ignore

class BaseRepository(Generic[ModelType]):
    
    def __init__(self,model:type[ModelType],db:AsyncSession):
        '''
        base repository for any type
        '''
        self._model = model
        self._db = db

    def _instance_to_dict(self,instance:ModelType) -> dict:
        return {
            key: getattr(instance, key)
            for key in instance.__mapper__.columns.keys()
            if hasattr(instance,key)
        }

    async def _get_instance_ignore_deleted(self,instance:ModelType) -> ModelType | None:
        '''
        gets an instance by eny of its unique fields

        this method must be implemented by direct childs of this class
        '''
        raise NotImplementedError()

    async def get_by_id(self,id:str,include_deleted:bool=False) -> ModelType | None:
        '''
        gets an instance by its id
        '''
        query = select(self._model)
        query = query.where((self._model.id==id) & (self._model.is_deleted != True)) if not include_deleted else query.where(self._model.id==id)
        result = await self._db.execute(
            query
        )
        return result.scalar_one_or_none()
    
    async def get_all(self,limit:int=100,skip:int=0,include_deleted:bool=False) -> Sequence[ModelType]:
        '''
        gets all the instances

        params:
            limit:int -> limit of results by response
            skip:int -> number of registers to skip
        '''
        query = select(self._model)
        query = query.where(self._model.is_deleted != True) if not include_deleted else query
        query = query.offset(skip).limit(limit)
        result = await self._db.execute(query)
        return result.scalars().all()
    
    async def create(self,instance:ModelType) -> ModelType | None:
        '''
        creates a new instance
        '''
        db_instance = await self._get_instance_ignore_deleted(instance)
        if db_instance is None:
            self._db.add(instance)
            await self._db.commit()
            await self._db.refresh(instance)
            return instance
        elif db_instance.is_deleted:
            db_instance.restore()
            update_data = self._instance_to_dict(db_instance)
            await self._db.execute(
                update(self._model).where(self._model.id==db_instance.id).values(**update_data)
            )
            await self._db.commit()
            await self._db.refresh(db_instance)
            return db_instance
        else:
            return None
        
    async def update(self,instance_id:str,update_instance:ModelType) -> ModelType | None:
        '''
        updates an instance
        '''
        db_instance = await self.get_by_id(instance_id)
        if db_instance is None:
            return None
        
        update_instance.created_at = db_instance.created_at
        update_instance.updated_at = db_instance.updated_at
        update_data = self._instance_to_dict(update_instance)
        await self._db.execute(
            update(self._model).where((self._model.is_deleted != True) & (self._model.id==instance_id)).values(**update_data)
        )
        await self._db.commit()
        await self._db.refresh(db_instance)
        
        return db_instance
    
    async def delete(self,instance_id:str) -> bool:
        '''
        deletes an instance
        '''
        db_instance = await self.get_by_id(instance_id)
        if db_instance is None:
            return False
        
        db_instance.soft_delete()
        await self._db.commit()
        await self._db.refresh(db_instance)
        
        return True