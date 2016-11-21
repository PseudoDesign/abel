from evelib.Sql import SqlObjectInterface


class CrestSqlInterface(SqlObjectInterface):
    @classmethod
    def create_from_crest_data(cls, crest_item, **kwargs):
        retval = cls.new_object_from_simple_crest(crest_item)
        if 'write' in kwargs:
            retval.write_to_db()
        return retval

    @classmethod
    def get_from_crest_by_id(cls, my_id):
        raise NotImplementedError()

    @classmethod
    def get_from_db_or_create(cls, my_id, crest_connection):
        pass
