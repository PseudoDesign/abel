import pycrest


class CrestConnection(pycrest.EVE):
    def __init__(self, **kwargs):
        self.__kwargs = kwargs
        super().__init__(**kwargs)
        self()
        
    def __str__(self):
        retval = ""
        retval += "Keyword Arguments:\n"
        for key in self.__kwargs:
            retval += "\t" + key + " : " + self.kwargs[key] + "\n"
        retval += "pycrest.EVE info:\n\t" + super().__str__()
        return retval

    @staticmethod
    def get_by_attr_value(objlist, attr, val):
        """ Searches list of dicts for a dict with dict[attr] == val """
        matches = [getattr(obj, attr) == val for obj in objlist]
        index = matches.index(True)  # find first match, raise ValueError if not found
        return objlist[index]

    @staticmethod
    def get_entries_in_page(page):
        ret = page().items
        while hasattr(page, 'next'):
            page = page().next()
            ret.extend(page().items)
        return ret


