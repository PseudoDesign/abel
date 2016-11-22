from sqlalchemy import String, Column, Integer
from evelib.Sql import SqlBase
from evelib.objects.CrestSqlInterface import CrestSqlInterface


class Region(SqlBase, CrestSqlInterface):
    __tablename__ = "region"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    @classmethod
    def get_objects_from_crest(cls, crest_connection):
        return crest_connection.regions
