from evelib.tests.test_Sql import TestSqlObjectBase
from evelib.objects.Station import Station
from evelib.Crest import CrestConnection
import yaml
import os


class TestStation(TestSqlObjectBase):
    TEST_OBJECT = Station

    @classmethod
    def setUpClass(cls):
        cls.eve = CrestConnection()

    def test_create_station(self):
        name = 'Jita IV - Moon 10 - Caldari Constructions Production Plant'
        new_obj = Station.create_new_object(self._connection.session, self.eve, 60002959, name, 30000142, write=True)
        self.assertEqual(name, new_obj.name)
        self.assertEqual(new_obj.r_solar_system.name, "Jita")

    def test_write_dict(self):
        with open(os.path.dirname(os.path.abspath(__file__))+"/staStations.yaml") as file:
            data = yaml.load(file)
        for entry in data:
            Station.new_object_from_dict(self._connection.session, self.eve, entry, write=True)
            self.assertIsNotNone(Station.get_from_db_by_id(self._connection.session, entry['stationID']))

