from evelib.tests.test_Sql import TestSqlObjectBase
from evelib.objects.Constellation import Constellation
from evelib.objects.Region import Region
from evelib.objects.tests.test_CrestSqlHelper import TestCrestSqlInterface


class TestConstellation(TestSqlObjectBase, TestCrestSqlInterface):
    TEST_OBJECT = Constellation

    SAMPLE_NAMES = [
        "Z6T6-B"
    ]

    def test_get_empty_solay_systems(self):
        TEST_ITEM = self.get_sample_object_name()
        crest_item = self.TEST_OBJECT.get_crest_item_by_attr(self.eve, "name", TEST_ITEM)
        constellation = self.TEST_OBJECT.get_db_item_by_crest_item(crest_item, create_if_null=True, write=True)
        self.assertEqual(len(constellation.r_solar_systems), 0)

    def test_region_references_constellation(self):
        TEST_ITEM = self.get_sample_object_name()
        crest_item = Constellation.get_crest_item_by_attr(self.eve, "name", TEST_ITEM)
        db_item = self.TEST_OBJECT.create_from_crest_data(crest_item, write=True)
        region = Region.get_from_db_by_id(db_item.region_id)
        self.assertEqual(region.id, db_item.region_id)
        self.assertEqual(region.name, db_item.r_region.name)
