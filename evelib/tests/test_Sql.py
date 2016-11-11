import unittest
from ..Sql import SqlConnection, SqlObject, Item


class TestSqlObjectBase(unittest.TestCase):
    DB_LOCATION = 'sqlite:///:memory:'
    TESTS = {}
    TEST_OBJECT = None
    _connection = None

    @classmethod
    def setUpClass(cls):
        cls._connection = SqlConnection(cls.DB_LOCATION)
        cls._connection.create_tables()

    def test_run_tests(self):
        """tests format: {test_method : [kwargs, dict(name='derp')]}"""
        for test in self.TESTS.keys():
            for kwargs in self.TESTS[test]:
                test(self.TEST_OBJECT, kwargs)

    def test_table_creation(self):
        """Verify our tablename exists in the database"""
        if self.TEST_OBJECT is not None:
            self.assertIn(self.TEST_OBJECT.__tablename__, self._connection.get_tables_in_db())

    def sql_object_creation_test(self, **kwargs):
        """Write an SQL object to the db and read it back"""
        columns = self.TEST_OBJECT.__table__.columns.keys()
        obj = self.TEST_OBJECT(**kwargs)
        obj.write_to_db()
        # Iterate through the kwargs to verify they were written to the table correctly
        for key, value in kwargs.items():
            self.assertEqual(obj.__getattribute__(key), value)
        self.assertIsNotNone(obj.id)
        read_obj = self.TEST_OBJECT.get_from_db_by_id(obj.id)
        self.assertIsNotNone(read_obj)
        # Iterate through the kwargs to verify they were written to the table correctly
        for key, value in kwargs.items():
            self.assertEqual(obj.__getattribute__(key), read_obj.__getattribute__(key))
        self.assertEqual(read_obj.id, obj.id)


class TestSql(TestSqlObjectBase):
    TEST_OBJECT = SqlObject
    TESTS = {
        TestSqlObjectBase.sql_object_creation_test: []
    }

    def test_sql_connection(self):
        self.assertIsNotNone(self._connection)
