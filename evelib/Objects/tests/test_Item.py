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
        super().setUpClass()

    def test_add_new_crest_item(self):
        crest_item = self.eve.get_by_attr_value(self.eve.get_entries_in_page(self.eve.itemTypes), 'name', 'Tritanium')()
        db_item = Item.create_from_crest_data(crest_item)
        db_item.write_to_db()
        TestCrestSqlHelper.compare_db_to_crest(self, db_item, crest_item)

    # TODO: Create a method to pull an entry from CREST if it doesn't exist in the db

class TestItemCrest(TestCrestObjectBase):
    pass
