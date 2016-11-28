from evelib.Sql import SqlObjectInterface


class CrestSqlInterface(SqlObjectInterface):
    @classmethod
    def create_from_crest_data(cls, crest_item, **kwargs):
        new_obj = cls.new_object_from_simple_crest(crest_item, **kwargs)
        if 'write' in kwargs:
            if kwargs['write']:
                new_obj.write_to_db()
                new_obj = cls.get_db_item_by_crest_item(crest_item, **kwargs)
        return new_obj

    @classmethod
    def crest_db_query(cls, crest_item, **kwargs):
        return cls.get_from_db_by_id(crest_item.id)

    @classmethod
    def get_db_item_by_crest_item(cls, crest_item, **kwargs):
        retval = cls.crest_db_query(crest_item, **kwargs)
        if retval is None:
            if 'create_if_null' in kwargs:
                if kwargs['create_if_null']:
                    retval = cls.create_from_crest_data(crest_item(), **kwargs)
        return retval

    @classmethod
    def is_crest_item_in_db(cls, crest_item):
        if cls.crest_db_query(crest_item) is not None:
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
    def get_from_db_or_crest_by_id(cls, crest_connection, id):
        retval = cls.get_from_db_by_id(id)
        if retval is None:
            item = cls.get_crest_item_by_attr(crest_connection, 'id', id)
            retval = cls.create_from_crest_data(item, write=True)
        return retval

    @classmethod
    def get_from_db_or_crest_by_name(cls, crest_connection, name):
        retval = cls.get_from_db_by_attr('name', name)
        if retval is None:
            item = cls.get_crest_item_by_attr(crest_connection, 'name', name)
            retval = cls.create_from_crest_data(item, write=True)
        return retval
