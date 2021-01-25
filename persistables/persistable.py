from collections import OrderedDict

from sqlalchemy.ext.declarative import declarative_base

from .manager import Manager
from .mixins import PersistableMixin


class Persistable(declarative_base(), PersistableMixin):

    def __repr__(self):
        fmt = '%Y-%m-%d %H:%M:%S'
        return f"Persistable(date={self.date.strftime(fmt)})"


def load_persistables(impl=Persistable,
                      database=None,
                      from_date=None,
                      to_date=None,
                      frequency=None,
                      compute_func=None):
    pass


def _internal_load_persistables(impl, database, timeline, compute_func):
    p_all = None
    manager = Manager(impl, database=database)
    with manager.open_session() as session:
        p_cached = session\
            .query(impl)\
            .filter(impl.date.in_(timeline))\
            .order_by(impl.date)\
            .all()
        p_new = [Persistable(date=date, data=compute_func(date))
                 for date in list(set(timeline)-{p.date for p in p_cached})]
        with session.begin():
            session.save_all(p_new)
        p_all = p_cached + p_new
    data = [p.data for p in sorted(p_all, key=lambda p: p.date)]
    return data


