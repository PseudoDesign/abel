from evelib.tests.test_Sql import TestSqlObjectBase
from evelib.objects.MarketDay import MarketDay, MarketDayDataSet
from evelib.objects.Item import Item
from evelib.objects.Region import Region
from datetime import datetime, timedelta
from evelib.objects.tests.test_CrestSqlHelper import TestCrestSqlInterface
from evelib.objects.tests.test_DataSetInterface import TestDataSetInterface
from evelib.Scraper import Scraper


class TestMarketDay(TestCrestSqlInterface):

    REGION_NAME = "The Forge"
    ITEM_NAME = "Tritanium"

    def setUp(self):
        super().setUp()
        self.item = Item.get_from_db_or_crest_by_name(self._connection.session, self.eve, self.ITEM_NAME)
        self.region = Region.get_from_db_or_crest_by_name(self._connection.session, self.eve, self.REGION_NAME)
        self.crest_kwargs = {
            "item": self.item,
            "region": self.region,
        }

    def test_add_new_crest_item(self):
        crest_item = MarketDay.get_crest_item_by_attr(
            self.eve, "date", MarketDay.date_to_string(datetime.now() + timedelta(days=-1)), self.crest_kwargs)
        db_item = MarketDay.create_from_crest_data(self._connection.session, crest_item, **self.crest_kwargs)
        db_item.write_to_db(self._connection.session)
        self.compare_db_to_crest(db_item, crest_item)

    def test_date_to_string(self):
        self.assertEqual(MarketDay.date_to_string(datetime(2016, 10, 21)), "2016-10-21T00:00:00")

    def test_is_crest_object_in_db(self):
        crest_item = MarketDay.get_crest_item_by_attr(
            self.eve, "date", MarketDay.date_to_string(datetime.now() + timedelta(days=-1)), self.crest_kwargs)
        self.assertFalse(MarketDay.is_crest_item_in_db(self._connection.session, crest_item, **self.crest_kwargs), "Item is already in database")
        MarketDay.create_from_crest_data(self._connection.session, crest_item, write=True, **self.crest_kwargs)
        self.assertTrue(MarketDay.is_crest_item_in_db(self._connection.session, crest_item, **self.crest_kwargs), "Item is not in database")

    def test_get_entry_or_add_from_crest(self):
        crest_item = MarketDay.get_crest_item_by_attr(
            self.eve, "date", MarketDay.date_to_string(datetime.now() + timedelta(days=-1)), self.crest_kwargs)
        self.assertFalse(MarketDay.is_crest_item_in_db(self._connection.session, crest_item, **self.crest_kwargs), "Item is already in database")
        db_item = MarketDay.get_db_item_by_crest_item(self._connection.session, crest_item, create_if_null=True, write=True, **self.crest_kwargs)
        self.assertEqual(db_item.volume, MarketDay.get_from_db_by_id(self._connection.session, db_item.id).volume)

    def test_get_db_item_by_name(self):
        crest_item = MarketDay.get_crest_item_by_attr(
            self.eve, "date", MarketDay.date_to_string(datetime.now() + timedelta(days=-1)), self.crest_kwargs)
        MarketDay.get_db_item_by_crest_item(self._connection.session, crest_item, create_if_null=True, write=True, **self.crest_kwargs)
        db_item = MarketDay.get_db_item_by_crest_item(self._connection.session, crest_item, create_if_null=True, write=True, **self.crest_kwargs)
        self.assertEqual(db_item.region_id, self.crest_kwargs['region'].id)


class TestMarketDayDataSet(TestDataSetInterface):
    REGION_NAME = "The Forge"
    ITEM_NAME = "Tritanium"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._connection.start_connection()
        item = Item.get_from_db_or_crest_by_name(cls._connection.session, cls.eve, cls.ITEM_NAME)
        region = Region.get_from_db_or_crest_by_name(cls._connection.session, cls.eve, cls.REGION_NAME)
        Scraper.update_market_day_data(cls._connection.session, region, item)

    def setUp(self):
        super().__init__()
        self.item = Item.get_from_db_or_crest_by_name(self._connection.session, self.eve, self.ITEM_NAME)
        self.region = Region.get_from_db_or_crest_by_name(self._connection.session, self.eve, self.REGION_NAME)

    def test_get_market_day_data_set(self):
        data_set = MarketDayDataSet.get_data_set(self._connection.session, self.region, self.item)
        self.assertGreater(len(data_set.x_data), 0)
        for entry in data_set.x_data:
            self.assertIs(type(entry), datetime)
        self.assertEqual(data_set['volume'].units, "Units")
        self.assertEqual(data_set['orderCount'].units, "Units")
        self.assertEqual(data_set['lowPrice'].units, "ISK")
        self.assertEqual(data_set['highPrice'].units, "ISK")
        self.assertEqual(data_set['avgPrice'].units, "ISK")
        self.assertEqual(data_set.x_data.units, "Time")

    def test_get_market_day_data_entries_by_units(self):
        data_set = MarketDayDataSet.get_data_set(self._connection.session, self.region, self.item)
        keys_by_units = data_set.get_entries_by_units()
        self.assertIn("ISK", keys_by_units)
        self.assertIn("Units", keys_by_units)
        self.assertIn("volume", keys_by_units["Units"])
        self.assertIn("orderCount", keys_by_units["Units"])
        self.assertIn("lowPrice", keys_by_units["ISK"])
        self.assertIn("highPrice", keys_by_units["ISK"])
        self.assertIn("avgPrice", keys_by_units["ISK"])
