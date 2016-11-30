import matplotlib
from evelib.objects.MarketDay import MarketDay


class DataSetEntry(list):

    def __init__(self, name, units):
        super().__init__()
        self.__dict__['units'] = units
        self.__dict__['name'] = name

    def __setattr__(self, key, value):
        raise AttributeError("Attributes in this class are read-only")


class MarketDayDataSet(dict):
    def __init__(self):
        super().__init__()
        self.x_data = DataSetEntry("Timestamp", "Time")
        self['volume'] = DataSetEntry("Volume", "Units")
        self['orderCount'] = DataSetEntry("Order Count", "Units")
        self['lowPrice'] = DataSetEntry("Low Price", "ISK")
        self['highPrice'] = DataSetEntry("High Price", "ISK")
        self['avgPrice'] = DataSetEntry("Average Price", "ISK")

class Plotter:

    def __init__(self):
        self.plot_data = []

    def add_data_set(self, data):
        pass

    def render(self, **kwargs):
        pass

    @staticmethod
    def get_market_day_data_sets(region, item):
        retval = MarketDayDataSet()
        return retval