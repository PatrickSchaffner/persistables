from copy import copy

from sqlalchemy import Column, func, Integer, PickleType, DateTime
from sqlalchemy.ext.declarative import declared_attr


class TablenameMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class IdMixin(object):
    id = Column(Integer, primary_key=True, autoincrement=True)


class DateIndexMixin(object):
    date = Column(DateTime, unique=True)


class RevisionDatesMixin(object):
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class DataMixin(object):
    data = Column(PickleType)

    def update_data(self):
        self.data = copy(self.data)


class PersistableMixin(TablenameMixin, IdMixin, DateIndexMixin, RevisionDatesMixin, DataMixin):
    pass

