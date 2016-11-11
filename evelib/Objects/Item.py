from sqlalchemy import String, Column, Integer
from evelib.Sql import SqlBase, SqlObjectInterface
from evelib.Crest import CrestObjectHelper


class Item(SqlBase, SqlObjectInterface, CrestObjectHelper):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String)