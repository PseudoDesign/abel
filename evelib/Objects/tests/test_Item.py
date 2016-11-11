from evelib.tests.test_Sql import TestSqlObjectBase
from evelib.Objects.Item import Item

class TestItem(TestSqlObjectBase):
    TEST_OBJECT = Item
    TESTS = {
        TestSqlObjectBase.sql_object_creation_test: [
            dict(name="TestItem"),
            dict(name="testItemWithNumb3r5")
        ]
    }
