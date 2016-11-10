import unittest
from ..Sql import SqlConnection, SqlObject, SqlBase, SqlSession


class Test(unittest.TestCase):
    DB_LOCATION = 'sqlite:///:memory:'
    connection = None

    @classmethod
    def setUpClass(cls):
        cls.connection = SqlConnection(cls.DB_LOCATION)
        cls.connection.create_tables()

    def test_sql_connection(self):
        self.assertIsNotNone(self.connection)

    def test_table_creation(self):
        """Verify our tablename exists in the database"""
        self.assertIn(SqlObject.__tablename__, self.connection.get_tables_in_db())

    def test_sql_object(self):
        """Write an SQL object to the db and read it back"""
        obj = SqlObject()
        obj.write_to_db()
        self.assertIsNotNone(obj.id)
        read_obj = SqlObject.get_from_db_by_id(obj.id)
        self.assertIsNotNone(read_obj)
        self.assertEqual(read_obj.id, obj.id)


