from evelib.Sql import SqlObjectInterface


class CrestSqlInterface(SqlObjectInterface):
    @classmethod
    def create_from_crest_data(cls, crest_item):
        return cls.new_object_from_simple_crest(crest_item)
