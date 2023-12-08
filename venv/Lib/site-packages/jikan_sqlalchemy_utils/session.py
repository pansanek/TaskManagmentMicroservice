import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .sqlalchemy_pysqlite_fixup import sqlalchemy_pysqlite_fixup

__all__ = ['SessionMaker']

class SessionMaker:
    def __init__(self, sessionmaker):
        self.sessionmaker = sessionmaker

    def __call__(self, *args, **kwargs):
        return self.sessionmaker(*args, **kwargs)

    @classmethod
    def from_engine(cls, engine):
        return cls(sessionmaker(bind=engine, autoflush=False))

    @classmethod
    def from_sqlite(cls, URI, *args, **kwargs):
        engine = create_engine(URI, *args, **kwargs)
        sqlalchemy_pysqlite_fixup(engine)
        return cls.from_engine(engine)

    @classmethod
    def from_uri_filename(cls, filename, *args, **kwargs):
        with open(filename, 'rt') as h:
            URI = h.read().strip()
        engine = create_engine(URI, *args, **kwargs)
        return cls.from_engine(engine)

    @classmethod
    def from_sqlite_filename(cls, filename, *args, **kwargs):
        return cls.from_sqlite('sqlite:///'+os.path.abspath(filename),
                               *args, **kwargs)

    def populate(self, Base):
        Base.metadata.create_all(self().bind)
