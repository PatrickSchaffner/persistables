from sqlalchemy import Column
from sqlalchemy.types import DateTime, Integer, PickleType
from sqlalchemy.ext.declarative import declared_attr, declarative_base


class TablenameMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

@declarative_base
class Base(object):
    pass

class Persistable(Base, TablenameMixin):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, unique=True)
    obj = Column(PickleType)
