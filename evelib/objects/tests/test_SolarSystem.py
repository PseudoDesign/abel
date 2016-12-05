from evelib.tests.test_Sql import TestSqlObjectBase
from evelib.objects.SolarSystem import SolarSystem
from evelib.objects.Constellation import Constellation
from evelib.objects.tests.test_CrestSqlHelper import TestCrestSqlInterface


class TestSolarSystem(TestCrestSqlInterface):
    TEST_OBJECT = SolarSystem

    SAMPLE_NAMES = [
        "Jita"
    ]

    def test_solar_system_references_constellation(self):
        TEST_ITEM = self.get_sample_object_name()
        crest_item = SolarSystem.get_crest_item_by_attr(self.eve, "name", TEST_ITEM)
        db_item = self.TEST_OBJECT.create_from_crest_data(self._connection.session, crest_item, write=True)
        constellation = Constellation.get_from_db_by_id(self._connection.session, db_item.constellation_id)
        self.assertEqual(constellation.id, db_item.constellation_id)
        self.assertEqual(constellation.name, db_item.r_constellation.name)

    def test_get_empty_stations(self):
        TEST_ITEM = self.get_sample_object_name()
        crest_item = self.TEST_OBJECT.get_crest_item_by_attr(self.eve, "name", TEST_ITEM)
        system = self.TEST_OBJECT.get_db_item_by_crest_item(self._connection.session, crest_item, create_if_null=True, write=True)
        self.assertEqual(len(system.r_stations), 0)