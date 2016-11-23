from evelib.tests.test_Sql import TestSqlObjectBase
from evelib.objects.Region import Region
from evelib.objects.tests.test_CrestSqlHelper import TestCrestSqlInterface


class TestRegion(TestSqlObjectBase, TestCrestSqlInterface):
    TEST_OBJECT = Region
    TESTS = {
        TestSqlObjectBase.sql_object_creation_test: [
            dict(name="TestItem"),
            dict(name="testItemWithNumb3r5"),
            dict(name="The Forge", description="some memes\n")
        ]
    }

    SAMPLE_NAMES = [
        "The Forge"
    ]

    def test_get_empty_constellations(self):
        TEST_ITEM = self.get_sample_object_name()
        crest_item = self.TEST_OBJECT.get_crest_item_by_attr(self.eve, "name", TEST_ITEM)
        region = self.TEST_OBJECT.get_db_item_by_crest_item(crest_item, create_if_null=True, write=True)
        self.assertEqual(len(region.r_constellations), 0)
