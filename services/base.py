from typing import Sequence,Generic,TypeVar
from pydantic import BaseModel as SchemasBaseModel
from database import BaseModel as ModelsBaseModel
from repositories import BaseRepository

ModelType = TypeVar('ModelType',bound=ModelsBaseModel) # type: ignore
RepositoryType = TypeVar('RepositoryType',bound=BaseRepository)
CreateSchemaType = TypeVar('CreateSchemaType',bound=SchemasBaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType',bound=SchemasBaseModel)
SchemaType = TypeVar('SchemaType',bound=SchemasBaseModel)

class BaseService(
    Generic[
        ModelType,
        CreateSchemaType,
        UpdateSchemaType,
        SchemaType,
        RepositoryType
    ]
):
    
    def __init__(self,model:type[ModelType],repository:RepositoryType):
        '''
        base service implementation for all services
        '''
        self._repository = repository
        self._model = model

    def _to_schema(self,model:ModelType) -> SchemaType:
        return model # type: ignore
    
    def _get_instance(self,**fields) -> ModelType:
        return self._model(**fields)
    
    async def get_by_id(self,instance_id:str,include_deleted:bool=False) -> SchemaType | None:
        '''
        gets an instance by its id
        '''
        model = await self._repository.get_by_id(instance_id,include_deleted)
        return self._to_schema(model) # type: ignore
    
    async def get_all(
        self,
        limit:int=100,
        skip:int=0,
        include_deleted:bool=False
    ) -> Sequence[SchemaType]:
        '''
        gets all the instances
        
        params:
            limit:int -> limit of results by response
            skip:int -> number of registers to skip
        '''
        results = await self._repository.get_all(limit,skip,include_deleted)
        return map(lambda model:self._to_schema(model),results) # type: ignore
    
    async def create(self,value:CreateSchemaType) -> SchemaType | None:
        '''
        creates a new instance
        '''
        db_instance = self._get_instance(**value.model_dump())
        return await self._repository.create(db_instance)
    
    async def update(
        self,
        instance_id:str,
        update_instance:UpdateSchemaType,
        **extra_values
    ) -> SchemaType | None:
        '''
        updates an instance
        '''
        instance = await self.get_by_id(instance_id)
        if instance is None:
            return None
        db_instance = self._get_instance(
            **{
                **update_instance.model_dump(),
                **extra_values,
                'id':instance_id
            }
        )
        return await self._repository.update(instance_id,db_instance)
    
    async def delete(self,instance_id:str) -> bool:
        '''
        deletes an instance
        '''
        return await self._repository.delete(instance_id)