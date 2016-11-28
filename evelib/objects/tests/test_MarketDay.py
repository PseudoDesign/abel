from evelib.tests.test_Sql import TestSqlObjectBase
from evelib.objects.MarketDay import MarketDay
from evelib.objects.Item import Item
from evelib.objects.Region import Region
from datetime import datetime, timedelta
from evelib.objects.tests.test_CrestSqlHelper import TestCrestSqlInterface


class TestMarketDay(TestSqlObjectBase, TestCrestSqlInterface):

    REGION_NAME = "The Forge"
    ITEM_NAME = "Tritanium"

    def setUp(self):
        super().setUp()
        self.item = Item.get_from_db_or_crest_by_name(self.eve, self.ITEM_NAME)
        self.region = Region.get_from_db_or_crest_by_name(self.eve, self.REGION_NAME)
        self.crest_kwargs = {
            "item": self.item,
            "region": self.region,
        }

    def test_add_new_crest_item(self):
        crest_item = MarketDay.get_crest_item_by_attr(
            self.eve, "date", MarketDay.date_to_string(datetime.now() + timedelta(days=-1)), self.crest_kwargs)
        db_item = MarketDay.create_from_crest_data(crest_item, **self.crest_kwargs)
        db_item.write_to_db()
        self.compare_db_to_crest(db_item, crest_item)

    def test_date_to_string(self):
        self.assertEqual(MarketDay.date_to_string(datetime(2016, 10, 21)), "2016-10-21T00:00:00")

    def test_is_crest_object_in_db(self):
        crest_item = MarketDay.get_crest_item_by_attr(
            self.eve, "date", MarketDay.date_to_string(datetime.now() + timedelta(days=-1)), self.crest_kwargs)
        self.assertFalse(MarketDay.is_crest_item_in_db(crest_item, **self.crest_kwargs), "Item is already in database")
        MarketDay.create_from_crest_data(crest_item, write=True, **self.crest_kwargs)
        self.assertTrue(MarketDay.is_crest_item_in_db(crest_item, **self.crest_kwargs), "Item is not in database")

    def test_get_entry_or_add_from_crest(self):
        crest_item = MarketDay.get_crest_item_by_attr(
            self.eve, "date", MarketDay.date_to_string(datetime.now() + timedelta(days=-1)), self.crest_kwargs)
        self.assertFalse(MarketDay.is_crest_item_in_db(crest_item, **self.crest_kwargs), "Item is already in database")
        db_item = MarketDay.get_db_item_by_crest_item(crest_item, create_if_null=True, write=True, **self.crest_kwargs)
        self.assertEqual(db_item.volume, MarketDay.get_from_db_by_id(db_item.id).volume)

"""
    def test_get_db_item_by_name(self):
        TEST_ITEM = self.get_sample_object_name()
        crest_item = MarketDay.get_crest_item_by_attr(self.eve, "name", TEST_ITEM)
        MarketDay.get_db_item_by_crest_item(crest_item, create_if_null=True, write=True)
        db_item = MarketDay.get_from_db_by_attr('name', TEST_ITEM)
        self.assertEqual(db_item.name, TEST_ITEM)

    def test_get_from_db_or_crest_by_id(self):
        TEST_ITEM = self.get_sample_object_name()
        crest_item = MarketDay.get_crest_item_by_attr(self.eve, "name", TEST_ITEM)
        new_id = crest_item.id
        from_crest = MarketDay.get_from_db_or_crest_by_id(self.eve, new_id)
        self.assertEqual(from_crest.name, TEST_ITEM)
        from_db = MarketDay.get_from_db_or_crest_by_id(self.eve, new_id)
        self.assertEqual(from_db.name, TEST_ITEM)
"""