import unittest
from ..Crest import CrestConnection


class TestCrestConnection(unittest.TestCase):
    def test_crest_connection(self):
        eve = CrestConnection()
        self.assertIsNotNone(eve._data)