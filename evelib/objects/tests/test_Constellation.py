from evelib.tests.test_Sql import TestSqlObjectBase
from evelib.objects.Constellation import Constellation
from evelib.objects.tests.test_CrestSqlHelper import TestCrestSqlInterface


class TestConstellation(TestSqlObjectBase, TestCrestSqlInterface):
    TEST_OBJECT = Constellation
    TESTS = {
        TestSqlObjectBase.sql_object_creation_test: [
            dict(name="TestItem"),
            dict(name="testItemWithNumb3r5")
        ]
    }

    SAMPLE_NAMES = [
        "Z6T6-B"
    ]


