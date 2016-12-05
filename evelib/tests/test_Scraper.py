import unittest
from evelib.objects.MarketDay import MarketDay
from evelib.objects.MarketOrder import MarketOrder
from evelib.Crest import CrestConnection
from evelib.Sql import SqlConnection
from evelib.objects.Item import Item
from evelib.objects.Region import Region
from evelib.Scraper import Scraper


class TestScraper(unittest.TestCase):

    REGION_NAME = "The Forge"
    ITEM_NAME = "Tritanium"

    @classmethod
    def setUpClass(cls):
        cls.eve = CrestConnection()

    def setUp(self):
        self._connection = SqlConnection()
        self._connection.create_tables()
        self._connection.start_connection()
        self.item = Item.get_from_db_or_crest_by_name(self._connection.session, self.eve, self.ITEM_NAME)
        self.region = Region.get_from_db_or_crest_by_name(self._connection.session, self.eve, self.REGION_NAME)

    def test_write_all_market_day_data(self):
        Scraper.update_market_day_data(self._connection.session, self.region, self.item)
        crest_items = MarketDay.get_objects_from_crest(self.eve, region=self.region, item=self.item).items
        for item in crest_items:
            self.assertTrue(MarketDay.is_crest_item_in_db(self._connection.session, item, region=self.region, item=self.item))

    def test_write_all_market_order_data(self):
        # There's a chance this test can fail due to timing issues
        Scraper.update_market_order_data(self._connection.session, self.region)
        crest_items = MarketOrder.get_objects_from_crest(self.eve, region=self.region)
        for item in crest_items:
            self.assertTrue(MarketOrder.is_crest_item_in_db(self._connection.session, item))
