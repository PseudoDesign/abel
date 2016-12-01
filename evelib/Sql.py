from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from threading import Lock


SqlBase = declarative_base()
SqlSession = sessionmaker()


class SqlConnection:
    def __init__(self,db='sqlite:///:memory:',echo=False):
        self.__db = db
        self.__echo = echo
        self.__engine = None
        self.__engine_lock = Lock()
        self.reset_engine()

    def reset_engine(self):
        # Can be used to reset an sqlite database in memory.  Useful for testing
        with self.__engine_lock:
            self.__engine = create_engine(self.__db, echo=self.__echo)
            SqlBase.metadata.bind = self.__engine
            SqlSession.configure(bind=self.__engine)

    def create_tables(self):
        with self.__engine_lock:
            SqlBase.metadata.create_all(self.__engine)

    def get_tables_in_db(self):
        with self.__engine_lock:
            return self.__engine.table_names()


class SqlObjectInterface:
    def write_to_db(self):
        session = SqlSession()
        session.add(self)
        session.commit()

    @classmethod
    def get_from_db_by_kwargs(cls, **kwargs):
        return cls.get_all_from_db_by_kwargs(**kwargs).first()

    @classmethod
    def get_all_from_db_by_kwargs(cls, **kwargs):
        session = SqlSession()
        return session.query(cls).filter_by(**kwargs)

    @classmethod
    def get_from_db_by_attr(cls, attr, key):
        return cls.get_from_db_by_kwargs(**{attr: key})

    @classmethod
    def get_from_db_by_id(cls, my_id):
        return cls.get_from_db_by_attr('id', my_id)

    @classmethod
    def new_object_from_crest(cls, crest, **kwargs):
        columns = dict()
        for column in cls.__table__.columns.keys():
            if hasattr(crest, column):
                columns[column] = getattr(crest, column)
        return cls(**columns)


class SqlTestObject(SqlBase, SqlObjectInterface):
    __tablename__ = 'undefined'

    id = Column(Integer, primary_key=True)
