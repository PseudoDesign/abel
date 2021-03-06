import unittest
from evelib.Sql import SqlConnection, SqlTestObject


class TestSqlObjectBase(unittest.TestCase):
    DB_LOCATION = 'sqlite:///:memory:'
    TESTS = {}
    TEST_OBJECT = None
    _connection = None

    def setUp(self):
        self._connection = SqlConnection(self.DB_LOCATION)
        self._connection.create_tables()
        self._connection.start_connection()

    def test_table_creation(self):
        """Verify our tablename exists in the database"""
        if self.TEST_OBJECT is not None:
            self.assertIn(self.TEST_OBJECT.__tablename__, self._connection.get_tables_in_db())

    def sql_object_creation_test(self, **kwargs):
        """Write an SQL object to the db and read it back"""
        columns = self.TEST_OBJECT.__table__.columns.keys()
        obj = self.TEST_OBJECT(**kwargs)
        obj.write_to_db(self._connection.session)
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
    TEST_OBJECT = SqlTestObject
    TESTS = {
        TestSqlObjectBase.sql_object_creation_test: [dict()]
    }

    def test_sql_connection(self):
        self.assertIsNotNone(self._connection)
