import unittest
from evelib.Crest import CrestConnection
from evelib.Sql import SqlConnection
from evelib.objects.Item import Item
from evelib.objects.Region import Region
from evelib.Scraper import Scraper
from evelib.Plotter import Plotter
from datetime import datetime


class TestPlotter(unittest.TestCase):
    REGION_NAME = "The Forge"
    ITEM_NAME = "Tritanium"

    @classmethod
    def setUpClass(cls):
        cls.eve = CrestConnection()
        cls._connection = SqlConnection()
        cls._connection.create_tables()
        cls.item = Item.get_from_db_or_crest_by_name(cls.eve, cls.ITEM_NAME)
        cls.region = Region.get_from_db_or_crest_by_name(cls.eve, cls.REGION_NAME)
        Scraper.update_market_day_data(cls.region, cls.item)

    def test_plot_all_market_day_data(self):
        plot_data = Plotter.get_market_day_data_set(self.region, self.item)
        plot = Plotter()
        plot.add_data_set(plot_data)
        plot.render()

    def test_get_market_day_data_set(self):
        data_set = Plotter.get_market_day_data_set(self.region, self.item)
        self.assertGreater(len(data_set.x_data), 0)
        for entry in data_set.x_data:
            self.assertIs(type(entry), datetime)
        self.assertEqual(data_set['volume'].units, "Units")
        self.assertEqual(data_set['orderCount'].units, "Units")
        self.assertEqual(data_set['lowPrice'].units, "ISK")
        self.assertEqual(data_set['highPrice'].units, "ISK")
        self.assertEqual(data_set['avgPrice'].units, "ISK")
        self.assertEqual(data_set.x_data.units, "Time")

