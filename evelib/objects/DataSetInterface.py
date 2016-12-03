class DataSetEntry(list):

    def __init__(self, name, units, scale=None):
        super().__init__()
        self.units = units
        self.name = name
        self.scale = scale


class DataSet(dict):

    # Name of what this data set entails.
    # Any values specific to a DataSet object should be
    # Set in "get_title"
    TITLE = None

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.x_data = None
        self.init_data_set_entries()

    def init_data_set_entries(self):
        raise NotImplementedError()

    def get_title(self):
        return self.TITLE

    def add_db_obj(self, obj):
        self.x_data += [obj.date]
        for key in self.keys():
            new_value = getattr(obj, key)
            if self[key]. scale is not None:
                new_value /= self[key]. scale
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
    def get_data_set(*args, **kwargs):
        raise NotImplementedError()
