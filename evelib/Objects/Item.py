from sqlalchemy import String, Column, Integer
from ..Sql import SqlBase, SqlObjectInterface


class Item(SqlBase, SqlObjectInterface):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String)