import unittest
from evelib.Crest import CrestConnection


class TestCrestObjectBase(unittest.TestCase):
    TESTS = {}
    TEST_OBJECT = None
    _connection = None

    @classmethod
    def setUpClass(cls):
        cls._connection = CrestConnection()

    def test_run_tests(self):
        """tests format: {test_method : [kwargs, dict(name='derp')]}"""
        for test in self.TESTS.keys():
            for kwargs in self.TESTS[test]:
                test(self, **kwargs)


class TestCrestObject(TestCrestObjectBase):
    def test_get_by_attr_value(self):
        # TODO: Write this test
        pass

    def test_get_all_items(self):
        # TODO: Write this test
        pass

    def test_crest_connection(self):
        eve = CrestConnection()
        self.assertIsNotNone(eve._data)
