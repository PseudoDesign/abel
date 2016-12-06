from sqlalchemy import String, Column, Integer, Boolean, Float
from evelib.Sql import SqlBase
from evelib.objects.CrestSqlInterface import CrestSqlInterface


class Item(SqlBase, CrestSqlInterface):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String(128, convert_unicode='force', unicode_error='backslashreplace'), nullable=False)
    published = Column(Boolean, nullable=False)
    mass = Column(Float, nullable=False)

    @classmethod
    def get_objects_from_crest(cls, crest_connection):
        return crest_connection.itemTypes
