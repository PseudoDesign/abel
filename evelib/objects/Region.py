from sqlalchemy import String, Column, Integer
from evelib.Sql import SqlBase
from evelib.objects.CrestSqlInterface import CrestSqlInterface


class Region(SqlBase, CrestSqlInterface):
    __tablename__ = "region"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)