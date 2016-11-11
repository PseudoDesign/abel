import evelib
from evelib.Objects.Item import Item


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
print(region.href)
print(item)
print(getAllItems(region().marketSellOrders(type=item.href)))

sql = evelib.SqlConnection()