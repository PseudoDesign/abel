import matplotlib.pyplot as plt
from evelib.objects.MarketDay import MarketDay


class DataSetEntry(list):

    def __init__(self, name, units, scale=None):
        super().__init__()
        self.__dict__['units'] = units
        self.__dict__['name'] = name
        self.__dict__['scale'] = scale

    def __setattr__(self, key, value):
        raise AttributeError("Attributes in this class are read-only")


class MarketDayDataSet(dict):

    TITLE = "Daily Market Data"

    def __init__(self):
        super().__init__()
        self.x_data = DataSetEntry("Timestamp", "Time")
        self['volume'] = DataSetEntry("Volume (10M)", "Units", 10000000)
        self['orderCount'] = DataSetEntry("Order Count", "Units")
        self['lowPrice'] = DataSetEntry("Low Price", "ISK")
        self['highPrice'] = DataSetEntry("High Price", "ISK")
        self['avgPrice'] = DataSetEntry("Average Price", "ISK")

    def add_entry(self, entry):
        self.x_data += [entry.date]
        for key in self.keys():
            new_value = getattr(entry, key)
            if self[key].scale is not None:
                new_value /= self[key].scale
            self[key] += [new_value]

    def get_entries_by_units(self):
        retval = {}
        for entry in self:
            if self[entry].units in retval:
                retval[self[entry].units] += [entry]
            else:
                retval[self[entry].units] = [entry]
        return retval

    @staticmethod
    def get_data_set(region, item):
        retval = MarketDayDataSet()
        for entry in MarketDay.get_all_from_db_by_kwargs(region_id=region.id, item_id=item.id):
            retval.add_entry(entry)
        return retval


class Plotter:
    def __init__(self):
        self.plot_data = []

    @staticmethod
    def draw_data_set(data_set):
        first = True
        units = data_set.get_entries_by_units()
        for unit in units:
            if first:
                first = False
                fig, x = plt.subplots()
                ax1 = x
                ax1.set_xlabel(data_set.x_data.units)
            else:
                x = ax1.twinx()
            for entry in units[unit]:
                x.plot(data_set.x_data, data_set[entry])
                x.set_ylabel(data_set[entry].units)
        plt.title(data_set.TITLE + " by " + data_set.x_data.name)
        plt.show()
