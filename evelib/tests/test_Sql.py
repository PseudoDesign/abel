import unittest
from ..Sql import SqlConnection, SqlObject, SqlBase, SqlSession


class TestSqlObjectBase(unittest.TestCase):
    DB_LOCATION = 'sqlite:///:memory:'
    TESTS = {}
    _connection = None

    @classmethod
    def setUpClass(cls):
        cls._connection = SqlConnection(cls.DB_LOCATION)
        cls._connection.create_tables()

    def test_run_tests(self):
        """tests format: {test_method : [[cls,[kwargs]], [Item,dict(name='derp')]]}"""
        for test in self.TESTS.keys():
            for val in self.TESTS[test]:
                print(test, val[0], val[1])
                test(val[0], val[1])

    def sql_object_creation_test(self, cls, **kwargs):
        """Write an SQL object to the db and read it back"""
        columns = cls.__table__.columns.keys()
        obj = cls(**kwargs)
        obj.write_to_db()
        # Iterate through the kwargs to verify they were written to the table correctly
        for key, value in kwargs.items():
            self.assertEqual(obj.__getattribute__(key), value)
        self.assertIsNotNone(obj.id)
        read_obj = cls.get_from_db_by_id(obj.id)
        self.assertIsNotNone(read_obj)
        # Iterate through the kwargs to verify they were written to the table correctly
        for key, value in kwargs.items():
            self.assertEqual(obj.__getattribute__(key), read_obj.__getattribute__(key))
        self.assertEqual(read_obj.id, obj.id)


class TestSql(TestSqlObjectBase):
    def test_sql_connection(self):
        self.assertIsNotNone(self._connection)

    def test_table_creation(self):
        """Verify our tablename exists in the database"""
        self.assertIn(SqlObject.__tablename__, self._connection.get_tables_in_db())

    def test_sql_object(self):
        """Write an SQL object to the db and read it back"""
        self.sql_object_creation_test(SqlObject)
