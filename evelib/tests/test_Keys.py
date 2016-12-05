import unittest
import os
from evelib.Keys import Keys, SqlKey


class TestKeys(unittest.TestCase):

    KEY_LOCATION = ".key_test.yaml"

    def setUp(self):
        try:
            os.remove(self.KEY_LOCATION)
        except OSError:
            pass

    def tearDown(self):
        try:
            os.remove(self.KEY_LOCATION)
        except OSError:
            pass

    def test_generate_keys(self):
        self.assertFalse(os.path.exists(self.KEY_LOCATION))
        with self.assertRaises(FileNotFoundError):
            Keys(self.KEY_LOCATION)
        Keys.generate_random_keys(self.KEY_LOCATION)
        with self.assertRaises(FileExistsError):
            Keys.generate_random_keys(self.KEY_LOCATION)
        keys = Keys(self.KEY_LOCATION)
        self.assertIs(type(keys.sql_user), str)
        self.assertEqual(len(keys.sql_user), 30)

    def test_generate_sql_key(self):
        key = SqlKey.create_random_key()
        self.assertIs(type(str(key)), str)
        self.assertEqual(len(str(key)), 30)
