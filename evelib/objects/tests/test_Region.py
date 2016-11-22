from evelib.tests.test_Sql import TestSqlObjectBase
from evelib.objects.Region import Region
from evelib.objects.tests.test_CrestSqlHelper import TestCrestSqlInterface


class TestRegion(TestSqlObjectBase):
    TEST_OBJECT = Region
    TESTS = {
        TestSqlObjectBase.sql_object_creation_test: [
            dict(name="TestItem"),
            dict(name="testItemWithNumb3r5"),
            dict(name="The Forge", description="some memes\n")
        ]
    }


