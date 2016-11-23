from sqlalchemy import String, Column, Integer
from evelib.Sql import SqlBase
from evelib.objects.CrestSqlInterface import CrestSqlInterface


class Constellation(SqlBase, CrestSqlInterface):
    __tablename__ = "constellation"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    @classmethod
    def get_objects_from_crest(cls, crest_connection):
        return crest_connection.constellations().items

    @classmethod
    def get_crest_item_by_attr(cls, crest_connection, attr, value):
        crest_item = crest_connection.get_by_attr_value(cls.get_objects_from_crest(crest_connection), attr, value)
        return crest_item

    @classmethod
    def get_db_item_by_crest_item(cls, crest_item, **kwargs):
        retval = cls.get_from_db_by_id(crest_item.id)
        if retval is None:
            if 'create_if_null' in kwargs:
                if kwargs['create_if_null']:
                    retval = cls.create_from_crest_data(crest_item, **kwargs)
        return retval
