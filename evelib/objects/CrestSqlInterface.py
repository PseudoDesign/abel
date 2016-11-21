from evelib.Sql import SqlObjectInterface


class CrestSqlInterface(SqlObjectInterface):
    @classmethod
    def create_from_crest_data(cls, crest_item, **kwargs):
        new_obj = cls.new_object_from_simple_crest(crest_item)
        if 'write' in kwargs:
            if kwargs['write']:
                new_obj.write_to_db()
        return new_obj

    @classmethod
    def get_db_item_by_crest_item(cls, crest_item, **kwargs):
        retval = cls.get_from_db_by_id(crest_item.id)
        if retval is None:
            if 'create_if_null' in kwargs:
                if kwargs['create_if_null']:
                    retval = cls.create_from_crest_data(crest_item, **kwargs)
        return retval
