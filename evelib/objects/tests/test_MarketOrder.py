from evelib.tests.test_Sql import TestSqlObjectBase
from evelib.objects.MarketOrder import MarketOrder
from evelib.Crest import CrestConnection
from evelib.objects.Region import Region
from evelib.objects.tests.test_CrestSqlHelper import TestCrestSqlInterface


class TestMarketOrder(TestCrestSqlInterface):

    REGION_NAME = "The Forge"

    @classmethod
    def setUpClass(cls):
        cls.eve = CrestConnection()
        super().setUpClass()

    def setUp(self):
        super().setUp()
        self.region = Region.get_from_db_or_crest_by_name(self._connection.session, self.eve, self.REGION_NAME)

    def test_add_new_crest_item(self):
        crest_item = MarketOrder.get_objects_from_crest(self.eve, region=self.region)[0]
        db_item = MarketOrder.create_from_crest_data(self._connection.session, crest_item)
        db_item.write_to_db(self._connection.session)
        self.compare_db_to_crest(db_item, crest_item)

    def test_is_crest_object_in_db(self):
        crest_item = MarketOrder.get_objects_from_crest(self.eve, region=self.region)[0]
        self.assertFalse(MarketOrder.is_crest_item_in_db(self._connection.session, crest_item), "Item is already in database")
        MarketOrder.create_from_crest_data(self._connection.session, crest_item, write=True)
        self.assertTrue(MarketOrder.is_crest_item_in_db(self._connection.session, crest_item), "Item is not in database")

    def test_get_entry_or_add_from_crest(self):
        crest_item = MarketOrder.get_objects_from_crest(self.eve, region=self.region)[0]
        self.assertFalse(MarketOrder.is_crest_item_in_db(self._connection.session, crest_item), "Item is already in database")
        db_item = MarketOrder.get_db_item_by_crest_item(self._connection.session, crest_item, create_if_null=True, write=True)
        self.assertEqual(db_item.volume, MarketOrder.get_from_db_by_id(self._connection.session, db_item.id).volume)


