import unittest
import os
from evelib.Keys import Keys


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

