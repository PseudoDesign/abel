from evelib.tests.test_Sql import TestSqlObjectBase
from evelib.objects.Station import Station
from evelib.Crest import CrestConnection
import random


class TestStation(TestSqlObjectBase):
    TEST_OBJECT = Station

    def get_sample_object_name(self):
        return random.choice(self.SAMPLE_NAMES)

    @classmethod
    def setUpClass(cls):
        cls.eve = CrestConnection()

    def test_create_station(self):
        name = 'Jita IV - Moon 10 - Caldari Constructions Production Plant'
        new_obj = Station.create_new_object(self.eve, 60002959, name, 30000142, write=True)
        self.assertEqual(name, new_obj.name)
