from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SqlBase = declarative_base()
SqlSession = sessionmaker()


class SqlConnection:
    def __init__(self,db='sqlite:///:memory:',echo=False):
        self.engine = create_engine(db,echo=echo)
        SqlBase.metadata.bind = self.engine
        SqlSession.configure(bind=self.engine)

    def create_tables(self):
        SqlBase.metadata.create_all(self.engine)

    def get_tables_in_db(self):
        return self.engine.table_names()


class SqlObjectInterface:
    def write_to_db(self):
        session = SqlSession()
        session.add(self)
        session.commit()

    @classmethod
    def get_from_db_by_kwargs(cls, **kwargs):
        session = SqlSession()
        return session.query(cls).filter_by(**kwargs).first()

    @classmethod
    def get_from_db_by_attr(cls, attr, key):
        return cls.get_from_db_by_kwargs(**{attr: key})

    @classmethod
    def get_from_db_by_id(cls, my_id):
        return cls.get_from_db_by_attr('id', my_id)

    @classmethod
    def new_object_from_simple_crest(cls, crest):
        columns = dict()
        for column in cls.__table__.columns.keys():
            columns[column] = getattr(crest, column)
        return cls(**columns)

class SqlTestObject(SqlBase, SqlObjectInterface):
    __tablename__ = 'undefined'

    id = Column(Integer, primary_key=True)