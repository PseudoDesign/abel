import matplotlib
from evelib.objects.MarketDay import MarketDay


class Plotter:
    class DataSet:
        def __init__(self, x, y, field_name="", x_name="", y_name=""):
            self.x = x
            self.y = y
            self.field_name = field_name
            self.x_name = x_name
            self.y_name = y_name

    def __init__(self):
        self.plot_data = []

    def add_data_set(self, data):
        pass

    def render(self, **kwargs):
        pass

    @staticmethod
    def get_market_day_data_sets(region, item):
        pass