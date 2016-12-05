from evelib.Scraper import Scraper
from evelib.objects.Item import Item
from evelib.objects.Region import Region
from evelib.Crest import CrestConnection
from evelib.Sql import SqlConnection
import time
import threading

REGION_NAMES = [
    "The Forge",
    ]
ITEM_NAMES = [
    "Tritanium",
    ]


def get_regions(crest_connection):
    regions = []
    for region in REGION_NAMES:
        regions += [Region.get_from_db_or_crest_by_name(crest_connection, region)]
    return regions


def get_items(crest_connection):
    items = []
    for item in ITEM_NAMES:
        items += [Item.get_from_db_or_crest_by_name(crest_connection, item)]
    return items


next_call = time.time()
minute_count = 60


def once_per_minute():
    _sql_connection = SqlConnection()
    _sql_connection.create_tables()
    crest_connection = CrestConnection()
    regions = get_regions(crest_connection)
    for region in regions:
        Scraper.update_market_order_data(region)
    print("Minute")


def once_per_hour():
    _sql_connection = SqlConnection()
    _sql_connection.create_tables()
    crest_connection = CrestConnection()
    regions = get_regions(crest_connection)
    items = get_items(crest_connection)
    for region in regions:
        for item in items:
            Scraper.update_market_day_data(region, item)
    print("Hour")


def scheduler():
    global next_call
    global minute_count
    next_call += 60
    once_per_minute()
    if minute_count >= 60:
        once_per_hour()
        minute_count = 0
    else:
        minute_count += 1
    threading.Timer(next_call - time.time(), scheduler).start()


def init_regions_and_items():
    crest_connection = CrestConnection()
    sql_connection = SqlConnection()
    sql_connection.create_tables()
    get_regions(crest_connection)
    get_items(crest_connection)


init_regions_and_items()
scheduler()
