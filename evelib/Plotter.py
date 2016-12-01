import matplotlib.pyplot as plt
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

    def add_entry(self, entry):
        self.x_data += [entry.date]
        for key in self.keys():
            self[key] += [getattr(entry, key)]

    def get_entries_by_units(self):
        retval = {}
        for entry in self:
            if self[entry].units in retval:
                retval[self[entry].units] += [entry]
            else:
                retval[self[entry].units] = [entry]
        return retval


class Plotter:
    def __init__(self):
        self.plot_data = []

    def add_plot(self, data):
        self.plot_data += [data]

    def add_data_set(self, plot_data):
        for entry in plot_data:
            self.add_plot({'x': plot_data.x_data, 'y': plot_data[entry]})

    def render(self, **kwargs):
        data = {}
        plt.show()

    @staticmethod
    def get_market_day_data_set(region, item):
        retval = MarketDayDataSet()
        for entry in MarketDay.get_all_from_db_by_kwargs(region_id=region.id, item_id=item.id):
            retval.add_entry(entry)
        return retval
