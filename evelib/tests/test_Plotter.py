import unittest
from evelib.Crest import CrestConnection
from evelib.Sql import SqlConnection
from evelib.objects.Item import Item
from evelib.objects.Region import Region
from evelib.Scraper import Scraper
from evelib.Plotter import Plotter


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
        plot_data = Plotter.get_market_day_plot_data(self.region, self.item)
        plot = Plotter()
        plot.add_data(plot_data)
        plot.render()
