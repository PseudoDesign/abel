import evelib


def getByAttrVal(objlist, attr, val):
    """ Searches list of dicts for a dict with dict[attr] == val """
    matches = [getattr(obj, attr) == val for obj in objlist]
    index = matches.index(True)  # find first match, raise ValueError if not found
    return objlist[index]


def getAllItems(page):
    ret = page().items
    while hasattr(page, 'next'):
        page = page().next()
        ret.extend(page().items)
    return ret


eve = evelib.CrestConnection()
print(eve)


region = getByAttrVal(eve.regions().items, 'name', 'The Forge')
item = getByAttrVal(getAllItems(eve.itemTypes), 'name', 'Tritanium')

const = getByAttrVal(eve.constellations().items, 'name', 'Z6T6-B')
print(const)
print(region)

sql = evelib.SqlConnection()