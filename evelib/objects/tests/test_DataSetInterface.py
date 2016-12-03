import unittest
from evelib.Crest import CrestConnection
from evelib.Scraper import Scraper
from evelib.Sql import SqlConnection


class TestDataSetInterface(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.eve = CrestConnection()
        cls._connection = SqlConnection()
        cls._connection.create_tables()