from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class Manager():
    
    def __init__(self,
                 base,
                 filename=':memory:',
                 protocol='sqlite',
                 echo=False):
        self._base = base
        self._db = protocol + ':///' + filename
        self._engine = create_engine(self._db, echo=echo)
        self._metadata = self._base.metadata
        self._session = None
        self._current = None
    
    def init(self):
        if self._session is not None:
            return
        self._metadata.create_all(bind=self._engine)
        self._session = sessionmaker(bind=self._engine)
    
    def session(self):
        self.init()
        return self._session()
    
    def __enter__(self):
        self._current = self.session()
        return self._current
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._current is None:
            return
        self._current.close()
        self._current = None


@classmethod
def _open(*args, **kwargs):
    return Manager(*args, **kwargs)


def create_base():
    base = declarative_base()
    base.open = _open
    return base
