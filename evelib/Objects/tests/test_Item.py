from evelib.tests.test_Sql import TestSqlObjectBase
from evelib.objects.Item import Item
from evelib.objects.tests.test_CrestSqlHelper import TestCrestSqlInterface


class TestItemSql(TestSqlObjectBase, TestCrestSqlInterface):
    TEST_OBJECT = Item
    TESTS = {
        TestSqlObjectBase.sql_object_creation_test: [
            dict(name="TestItem"),
            dict(name="testItemWithNumb3r5")
        ]
    }

