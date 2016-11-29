from evelib.tests.test_Sql import TestSqlObjectBase
from evelib.objects.MarketOrder import MarketOrder
from evelib.Crest import CrestConnection
from evelib.objects.Region import Region
from evelib.objects.tests.test_CrestSqlHelper import TestCrestSqlInterface


class TestMarketOrder(TestSqlObjectBase, TestCrestSqlInterface):

    REGION_NAME = "The Forge"

    @classmethod
    def setUpClass(cls):
        cls.eve = CrestConnection()
        super().setUpClass()

    def setUp(self):
        self.region = Region.get_from_db_or_crest_by_name(self.eve, self.REGION_NAME)

    def test_add_new_crest_item(self):
        crest_item = MarketOrder.get_objects_from_crest(self.eve, region=self.region)[0]
        db_item = MarketOrder.create_from_crest_data(crest_item)
        db_item.write_to_db()
        self.compare_db_to_crest(db_item, crest_item)
