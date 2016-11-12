from sqlalchemy import String, Column, Integer, Boolean, Float
from evelib.Sql import SqlBase
from evelib.objects.CrestSqlInterface import CrestSqlInterface


class Item(SqlBase, CrestSqlInterface):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    published = Column(Boolean)
    mass = Float()
