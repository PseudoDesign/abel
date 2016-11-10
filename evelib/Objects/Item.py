from sqlalchemy import String, Column
from ..Sql import SqlObject


class Item(SqlObject):
    __tablename__ = "item"

    name = Column(String)