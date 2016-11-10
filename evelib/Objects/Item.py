from ..Sql import SqlObject
from sqlalchemy import String, Column


class Item(SqlObject):
    __tablename__ = "item"

    name = Column(String)