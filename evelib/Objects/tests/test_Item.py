from evelib.tests.test_Sql import TestSqlObjectBase
from evelib.tests.test_Crest import TestCrestObjectBase
from evelib.Crest import CrestConnection
from evelib.objects.Item import Item
from evelib.objects.tests.test_CrestSqlHelper import TestCrestSqlHelper


class TestItemSql(TestSqlObjectBase):
    TEST_OBJECT = Item
    TESTS = {
        TestSqlObjectBase.sql_object_creation_test: [
            dict(name="TestItem"),
            dict(name="testItemWithNumb3r5")
        ]
    }

    @classmethod
    def setUpClass(cls):
        cls.eve = CrestConnection()

    def setUp(self):
        super().setUp()

    def test_add_new_crest_item(self):
        crest_item = self.eve.get_by_attr_value(self.eve.get_entries_in_page(self.eve.itemTypes), 'name', 'Tritanium')()
        db_item = Item.create_from_crest_data(crest_item)
        db_item.write_to_db()
        TestCrestSqlHelper.compare_db_to_crest(self, db_item, crest_item)

    def test_is_crest_object_in_db(self):
        TEST_ITEM = "Pyerite"
        crest_item = self.eve.get_by_attr_value(self.eve.get_entries_in_page(self.eve.itemTypes), 'name', TEST_ITEM)()
        self.assertFalse(Item.is_crest_item_in_db(crest_item), "Item is already in database")
        Item.create_from_crest_data(crest_item, write=True)
        self.assertTrue(Item.is_crest_item_in_db(crest_item), "Item is not in database")

    def test_get_entry_or_add_from_crest(self):
        # Create a method to pull an entry from CREST if it doesn't exist in the db
        TEST_ITEM = "Veldspar"
        crest_item = self.eve.get_by_attr_value(self.eve.get_entries_in_page(self.eve.itemTypes), 'name', TEST_ITEM)()
        self.assertFalse(Item.is_crest_item_in_db(crest_item), "Item is already in database")
        db_item = Item.get_db_item_by_crest_item(crest_item, create_if_null=True, write=True)
        self.assertEqual(db_item.name, Item.get_from_db_by_id(db_item.id).name)

    def test_get_db_item_by_name(self):
        TEST_ITEM = "Plagioclase"
        crest_item = self.eve.get_by_attr_value(self.eve.get_entries_in_page(self.eve.itemTypes), 'name', TEST_ITEM)()
        Item.get_db_item_by_crest_item(crest_item, create_if_null=True, write=True)
        db_item = Item.get_from_db_by_attr('name', TEST_ITEM)
        self.assertEqual(db_item.name, TEST_ITEM)

