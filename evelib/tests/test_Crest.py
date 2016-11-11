import unittest
from evelib.Crest import CrestConnection


class TestCrestConnection(unittest.TestCase):
    def test_crest_connection(self):
        eve = CrestConnection()
        self.assertIsNotNone(eve._data)


class TestCrestObjectInterface(unittest.TestCase):
    def test_get_by_attr_value(self):
        # TODO: Write this test
        pass

    def test_get_all_items(self):
        # TODO: Write this test
        pass
