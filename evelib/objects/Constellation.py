from sqlalchemy import String, Column, Integer
from evelib.Sql import SqlBase
from evelib.objects.CrestSqlInterface import CrestSqlInterface


class Constellation(SqlBase, CrestSqlInterface):
    __tablename__ = "constellation"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    @classmethod
    def get_objects_from_crest(cls, crest_connection):
        return crest_connection.constellations

    @classmethod
    def get_crest_item_by_attr(cls, crest_connection, attr, value):
        crest_item = crest_connection.get_by_attr_value(
            crest_connection.get_entries_in_page(cls.get_objects_from_crest(crest_connection)), attr, value)
        return crest_item