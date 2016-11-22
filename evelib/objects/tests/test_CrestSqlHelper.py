from evelib.Crest import CrestConnection
import unittest


class TestCrestSqlInterface(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.eve = CrestConnection()

    def compare_db_to_crest(self, db, crest):
        for column in db.__table__.columns.keys():
            self.assertEqual(getattr(db, column), getattr(crest, column))
