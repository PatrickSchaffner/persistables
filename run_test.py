from contextlib import contextmanager
from datetime import datetime, timedelta
from copy import copy

import numpy as np

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, DateTime, PickleType
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class TablenameMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

class Persistable(declarative_base(), TablenameMixin):
    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(DateTime, unique=True)
    data = Column(PickleType(comparator=lambda a, b: a is b))
    
    def update_data(self):
        self.data = copy(self.data)
    
    def __repr__(self):
        return f"Persistable(id={self.id}, date={self.date.strftime('%Y-%m-%d %H:%M:%S')}, data={str(self.data)})"


engine = create_engine('sqlite:///test.db', echo=True)
Persistable.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine)

@contextmanager
def open_session():
    s = session()
    try:
        yield s
        s.commit()
    except:
        s.rollback()
        raise
    finally:
        s.close()

with open_session() as s:
    p_all = s.query(Persistable).filter(Persistable.date>datetime.now()-timedelta(minutes=20)).all()
    print(f"Found {len(p_all)} persistables.")
    for p in p_all:
        print(p)
        if isinstance(p.data, dict):
            p.data['looked_at'] = datetime.now()
            p.update_data()
    p_new = Persistable(date=datetime.now(), data=np.random.randint(0,10,(2,3)))
    s.add(p_new)
    s.commit()

print(sqlalchemy.__version__)
