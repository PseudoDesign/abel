from sqlalchemy import String, Column, Integer, Boolean, Float
from evelib.Sql import SqlBase, SqlObjectInterface


class Item(SqlBase, SqlObjectInterface):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    published = Column(Boolean)
    mass = Float()

    @classmethod
    def create_from_crest_data(cls, crest_item):
        return cls.new_object_from_simple_crest(crest_item)
