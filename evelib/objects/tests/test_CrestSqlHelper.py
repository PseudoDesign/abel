from evelib.Crest import CrestConnection
import unittest


class TestCrestSqlInterface(unittest.TestCase):
    TEST_OBJECT = None

    @classmethod
    def setUpClass(cls):
        cls.eve = CrestConnection()

    def compare_db_to_crest(self, db, crest):
        for column in db.__table__.columns.keys():
            self.assertEqual(getattr(db, column), getattr(crest, column))

    def test_add_new_crest_item(self):
        if self.TEST_OBJECT is not None:
            crest_item = self.TEST_OBJECT.get_crest_item_by_attr(self.eve, "name", "Tritanium")
            db_item = self.TEST_OBJECT.create_from_crest_data(crest_item)
            db_item.write_to_db()
            self.compare_db_to_crest(db_item, crest_item)

    def test_is_crest_object_in_db(self):
        if self.TEST_OBJECT is not None:
            TEST_ITEM = "Pyerite"
            crest_item = self.TEST_OBJECT.get_crest_item_by_attr(self.eve, "name", TEST_ITEM)
            self.assertFalse(self.TEST_OBJECT.is_crest_item_in_db(crest_item), "Item is already in database")
            self.TEST_OBJECT.create_from_crest_data(crest_item, write=True)
            self.assertTrue(self.TEST_OBJECT.is_crest_item_in_db(crest_item), "Item is not in database")

    def test_get_entry_or_add_from_crest(self):
        if self.TEST_OBJECT is not None:
            TEST_ITEM = "Veldspar"
            crest_item = self.eve.get_by_attr_value(self.eve.get_entries_in_page(self.eve.itemTypes), 'name', TEST_ITEM)()
            self.assertFalse(self.TEST_OBJECT.is_crest_item_in_db(crest_item), "Item is already in database")
            db_item = self.TEST_OBJECT.get_db_item_by_crest_item(crest_item, create_if_null=True, write=True)
            self.assertEqual(db_item.name, self.TEST_OBJECT.get_from_db_by_id(db_item.id).name)

    def test_get_db_item_by_name(self):
        if self.TEST_OBJECT is not None:
            TEST_ITEM = "Plagioclase"
            crest_item = self.eve.get_by_attr_value(self.eve.get_entries_in_page(self.eve.itemTypes), 'name', TEST_ITEM)()
            self.TEST_OBJECT.get_db_item_by_crest_item(crest_item, create_if_null=True, write=True)
            db_item = self.TEST_OBJECT.get_from_db_by_attr('name', TEST_ITEM)
            self.assertEqual(db_item.name, TEST_ITEM)