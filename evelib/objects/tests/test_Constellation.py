from evelib.tests.test_Sql import TestSqlObjectBase
from evelib.objects.Constellation import Constellation
from evelib.objects.tests.test_CrestSqlHelper import TestCrestSqlInterface


class TestConstellation(TestSqlObjectBase, TestCrestSqlInterface):
    TEST_OBJECT = Constellation

    SAMPLE_NAMES = [
        "Z6T6-B"
    ]


