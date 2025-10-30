from sqlalchemy import Column,DateTime,Boolean,func
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime,timezone

class TimestampMixin:
    '''
    mixin to add fields created_at and updated_at
    '''

    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),nullable=False)
    
    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc),nullable=False)

class SoftDeleteMixin:
    '''
    mixin to add soft-delete functionality
    '''

    is_deleted = Column(Boolean,default=False,nullable=False)
    deleted_at = Column(DateTime(timezone=True),nullable=True)

    def soft_delete(self):
        '''
        marks this element as deleted
        '''
        self.is_deleted = True
        self.deleted_at = lambda:datetime.now(timezone.utc)
    
    def restore(self):
        '''
        restores this element
        '''
        self.is_deleted = False
        self.deleted_at = None