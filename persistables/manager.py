from contextlib import contextmanager

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker


class Manager(object):

    def __init__(self, base, database='sqlite:///:memory:', echo=False):
        self._engine = create_engine(database, echo=echo)
        self._metadata = base.metadata
        self._session = sessionmaker(bind=self._engine, expire_on_commit=False)
        self._initialized = False

    @property
    def engine(self):
        return self._engine

    @property
    def session(self):
        return self._session

    @property
    def metadata(self):
        return self._metadata

    def open_connection(self):
        self._initialize_db()
        return self._engine.connect()

    @contextmanager
    def open_session(self, auto_commit=False):
        self._initialize_db()
        session = self._session(expire_on_commit=False)
        try:
            yield session
            if auto_commit:
                session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()

    def _initialize_db(self):
        if self._initialized:
            return
        self._metadata.create_all(bind=self._engine)
