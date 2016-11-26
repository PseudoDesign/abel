from evelib.tests.test_Sql import TestSqlObjectBase
from evelib.objects.SolarSystem import SolarSystem
from evelib.objects.Constellation import Constellation
from evelib.objects.tests.test_CrestSqlHelper import TestCrestSqlInterface


class TestSolarSystem(TestSqlObjectBase, TestCrestSqlInterface):
    TEST_OBJECT = SolarSystem

    SAMPLE_NAMES = [
        "Jita"
    ]

    def test_solar_system_references_region(self):
        TEST_ITEM = self.get_sample_object_name()
        crest_item = SolarSystem.get_crest_item_by_attr(self.eve, "name", TEST_ITEM)
        db_item = self.TEST_OBJECT.create_from_crest_data(crest_item, write=True)
        constellation = Constellation.get_from_db_by_id(db_item.constellation_id)
        self.assertEqual(constellation.id, db_item.constellation_id)
        self.assertEqual(constellation.name, db_item.r_constellation.name)