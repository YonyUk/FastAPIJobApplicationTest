from typing import Sequence,Generic,TypeVar,Callable
from pydantic import BaseModel as SchemasBaseModel
from abc import ABC,abstractmethod
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
    
    def __init__(
            self,
            model:type[ModelType],
            repository:RepositoryType,
            exclude_fields:set=set(),
            exclude_unset:bool=True
        ):
        '''
        base service implementation for all services
        '''
        self._repository = repository
        self._model = model
        self._exclude_fields = exclude_fields
        self._exclude_unset = exclude_unset

    async def _to_schema(self,model:ModelType) -> SchemaType:
        return model # type: ignore
    
    def _get_instance(self,**fields) -> ModelType:
        return self._model(**fields)
    
    async def _process_before_update(
        self,
        update_data:UpdateSchemaType,
        existing_model:ModelType,
        **extra_fields
    ) -> ModelType:
        # creates the instance with the updated data
        db_instance = self._get_instance(
            **{
                **update_data.model_dump(
                    exclude=self._exclude_fields,
                    exclude_unset=self._exclude_unset
                ),
                **extra_fields
            }
        )
        # modify the updated instance
        return await self._process_before_update_modifier(update_data,existing_model,db_instance)
    
    async def _process_before_create(
        self,
        instance:ModelType,
        create_value:CreateSchemaType
    ) -> ModelType:
        return instance

    @abstractmethod
    async def _process_before_update_modifier(
        self,
        update_data:UpdateSchemaType,
        existing_model:ModelType,
        model:ModelType
    ) -> ModelType:
        raise NotImplementedError()
    
    async def get_by_id(self,instance_id:str,include_deleted:bool=False) -> SchemaType | None:
        '''
        gets an instance by its id
        '''
        model = await self._repository.get_by_id(instance_id,include_deleted)
        return await self._to_schema(model) # type: ignore
    
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
        instances = []
        for result in results:
            ins = await self._to_schema(result)
            instances.append(ins)
        return instances
    
    async def create(self,value:CreateSchemaType,**extra_fields) -> SchemaType | None:
        '''
        creates a new instance
        '''
        db_instance = self._get_instance(
            **{
                **value.model_dump(
                    exclude=self._exclude_fields,
                    exclude_unset=self._exclude_unset
                ),
                **extra_fields
            }
        )
        db_instance = await self._process_before_create(db_instance,value)
        result = await self._repository.create(db_instance)
        if result is None:
            return None
        return await self._to_schema(result)
    
    async def update(
        self,
        instance_id:str,
        update_instance:UpdateSchemaType,
        **extra_values
    ) -> SchemaType | None:
        '''
        updates an instance
        '''
        existing_instance = await self._repository.get_by_id(instance_id)
        if existing_instance is None:
            return None
        db_instance = await self._process_before_update(
            update_instance,
            existing_instance,
            **{**extra_values,'id':instance_id}
        )
        return await self._repository.update(instance_id,db_instance)
    
    async def delete(self,instance_id:str) -> bool:
        '''
        deletes an instance
        '''
        return await self._repository.delete(instance_id)