from evelib.tests.test_Sql import TestSqlObjectBase
from evelib.tests.test_Crest import TestCrestObjectBase
from evelib.Crest import CrestConnection
from evelib.objects.Item import Item


class TestItemSql(TestSqlObjectBase):
    TEST_OBJECT = Item
    TESTS = {
        TestSqlObjectBase.sql_object_creation_test: [
            dict(name="TestItem"),
            dict(name="testItemWithNumb3r5")
        ]
    }

    def test_add_all_items_to_db(self):
        eve = CrestConnection()


class TestItemCrest(TestCrestObjectBase):
    pass
