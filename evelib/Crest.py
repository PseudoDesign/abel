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
