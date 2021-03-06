from evelib.Sql import SqlObjectInterface
from datetime import datetime


class CrestSqlInterface(SqlObjectInterface):

    CREST_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

    @classmethod
    def create_from_crest_data(cls, sql_session, crest_item, **kwargs):
        new_obj = cls.new_object_from_crest(crest_item, **kwargs)
        if 'write' in kwargs:
            if kwargs['write']:
                new_obj.write_to_db(sql_session)
                new_obj = cls.get_db_item_by_crest_item(sql_session, crest_item, **kwargs)
        return new_obj

    @classmethod
    def crest_db_query(cls, sql_session, crest_item, **kwargs):
        return cls.get_from_db_by_id(sql_session, crest_item.id)

    @classmethod
    def get_db_item_by_crest_item(cls, sql_session, crest_item, **kwargs):
        retval = cls.crest_db_query(sql_session, crest_item, **kwargs)
        if retval is None:
            if 'create_if_null' in kwargs:
                if kwargs['create_if_null']:
                    retval = cls.create_from_crest_data(sql_session, crest_item(), **kwargs)
        return retval

    @classmethod
    def is_crest_item_in_db(cls, sql_session, crest_item):
        if cls.crest_db_query(sql_session, crest_item) is not None:
            return True
        return False

    @classmethod
    def get_objects_from_crest(cls, crest_connection):
        raise NotImplementedError()

    @classmethod
    def get_crest_item_by_attr(cls, crest_connection, attr, value, object_kwargs={}, **kwargs):
        crest_item = crest_connection.get_by_attr_value(
            crest_connection.get_entries_in_page(
                cls.get_objects_from_crest(crest_connection, **object_kwargs)), attr, value)
        if 'dereference' not in kwargs or kwargs['dereference']:
                    crest_item = crest_item()
        return crest_item

    @classmethod
    def get_from_db_or_crest_by_id(cls, sql_session, crest_connection, id):
        retval = cls.get_from_db_by_id(sql_session, id)
        if retval is None:
            item = cls.get_crest_item_by_attr(crest_connection, 'id', id)
            retval = cls.create_from_crest_data(sql_session, item, write=True)
        return retval

    @classmethod
    def get_from_db_or_crest_by_name(cls, sql_session, crest_connection, name):
        retval = cls.get_from_db_by_attr(sql_session, 'name', name)
        if retval is None:
            item = cls.get_crest_item_by_attr(crest_connection, 'name', name)
            retval = cls.create_from_crest_data(sql_session, item, write=True)
        return retval

    @classmethod
    def date_to_string(cls, dt):
        # "2016-10-21T00:00:00"
        # Note that the time is always 00:00:00 eve time
        return dt.strftime(cls.CREST_TIME_FORMAT)

    @classmethod
    def string_to_datetime(cls, my_string):
        return datetime.strptime(my_string, cls.CREST_TIME_FORMAT)
