from sqlalchemy import String, Column, Integer, Boolean, Float
from evelib.Sql import SqlBase
from evelib.objects.CrestSqlInterface import CrestSqlInterface


class Item(SqlBase, CrestSqlInterface):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    published = Column(Boolean)
    mass = Float()

    @classmethod
    def is_crest_item_in_db(cls, crest_item):
        if cls.get_from_db_by_id(crest_item.id) is not None:
            return True
        return False

    @classmethod
    def get_db_item_by_crest_obj(cls, crest_item, **kwargs):
        pass

