from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SqlBase = declarative_base()
SqlSession = sessionmaker()


class SqlConnection:
    def __init__(self,db='sqlite:///:memory:', echo=False):
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
    def get_from_db_by_id(cls, my_id):
        session = SqlSession()
        return session.query(cls).filter_by(id=my_id).first()


class SqlTestObject(SqlBase, SqlObjectInterface):
    __tablename__ = 'undefined'

    id = Column(Integer, primary_key=True)