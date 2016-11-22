from sqlalchemy import String, Column, Integer, Float
from evelib.Sql import SqlBase
from evelib.objects.CrestSqlInterface import CrestSqlInterface


class Constellation(SqlBase, CrestSqlInterface):
    __tablename__ = "constellation"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    @classmethod
    def get_objects_from_crest(cls, crest_connection):
        return crest_connection.regions
