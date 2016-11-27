from evelib.Crest import CrestConnection
import unittest
import random


class TestCrestSqlInterface(unittest.TestCase):
    TEST_OBJECT = None
    SAMPLE_NAMES = None

    def get_sample_object_name(self):
        return random.choice(self.SAMPLE_NAMES)

    @classmethod
    def setUpClass(cls):
        cls.eve = CrestConnection()

    def compare_db_to_crest(self, db, crest):
        for column in db.__table__.columns.keys():
            if hasattr(crest, column):
                self.assertEqual(getattr(db, column), getattr(crest, column))

    def test_add_new_crest_item(self):
        if self.TEST_OBJECT is not None:
            TEST_ITEM = self.get_sample_object_name()
            crest_item = self.TEST_OBJECT.get_crest_item_by_attr(self.eve, "name", TEST_ITEM)
            db_item = self.TEST_OBJECT.create_from_crest_data(crest_item)
            db_item.write_to_db()
            self.compare_db_to_crest(db_item, crest_item)

    def test_is_crest_object_in_db(self):
        if self.TEST_OBJECT is not None:
            TEST_ITEM = self.get_sample_object_name()
            crest_item = self.TEST_OBJECT.get_crest_item_by_attr(self.eve, "name", TEST_ITEM)
            self.assertFalse(self.TEST_OBJECT.is_crest_item_in_db(crest_item), "Item is already in database")
            self.TEST_OBJECT.create_from_crest_data(crest_item, write=True)
            self.assertTrue(self.TEST_OBJECT.is_crest_item_in_db(crest_item), "Item is not in database")

    def test_get_entry_or_add_from_crest(self):
        if self.TEST_OBJECT is not None:
            TEST_ITEM = self.get_sample_object_name()
            crest_item = self.TEST_OBJECT.get_crest_item_by_attr(self.eve, "name", TEST_ITEM)
            self.assertFalse(self.TEST_OBJECT.is_crest_item_in_db(crest_item), "Item is already in database")
            db_item = self.TEST_OBJECT.get_db_item_by_crest_item(crest_item, create_if_null=True, write=True)
            self.assertEqual(db_item.name, self.TEST_OBJECT.get_from_db_by_id(db_item.id).name)

    def test_get_db_item_by_name(self):
        if self.TEST_OBJECT is not None:
            TEST_ITEM = self.get_sample_object_name()
            crest_item = self.TEST_OBJECT.get_crest_item_by_attr(self.eve, "name", TEST_ITEM)
            self.TEST_OBJECT.get_db_item_by_crest_item(crest_item, create_if_null=True, write=True)
            db_item = self.TEST_OBJECT.get_from_db_by_attr('name', TEST_ITEM)
            self.assertEqual(db_item.name, TEST_ITEM)

    def test_get_from_db_or_crest_by_id(self):
        if self.TEST_OBJECT is not None:
            TEST_ITEM = self.get_sample_object_name()
            crest_item = self.TEST_OBJECT.get_crest_item_by_attr(self.eve, "name", TEST_ITEM)
            new_id = crest_item.id
            from_crest = self.TEST_OBJECT.get_from_db_or_crest_by_id(self.eve, new_id)
            self.assertEqual(from_crest.name, TEST_ITEM)
            from_db = self.TEST_OBJECT.get_from_db_or_crest_by_id(self.eve, new_id)
            self.assertEqual(from_db.name, TEST_ITEM)

    def test_get_from_db_or_crest_by_name(self):
        if self.TEST_OBJECT is not None:
            TEST_ITEM = self.get_sample_object_name()
            from_crest = self.TEST_OBJECT.get_from_db_or_crest_by_name(self.eve, TEST_ITEM)
            self.assertEqual(from_crest.name, TEST_ITEM)
            from_db = self.TEST_OBJECT.get_from_db_or_crest_by_name(self.eve, TEST_ITEM)
            self.assertEqual(from_db.name, TEST_ITEM)

