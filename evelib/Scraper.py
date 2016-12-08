from evelib.objects.MarketDay import MarketDay
from evelib.objects.MarketOrder import MarketOrder
from evelib.Crest import CrestConnection
from evelib.objects.Item import Item


class Scraper:

    @staticmethod
    def update_market_day_data(sql_session, region, item):
        eve = CrestConnection()
        crest_items = MarketDay.get_objects_from_crest(eve, region=region, item=item).items
        for crest_item in crest_items:
            if not MarketDay.is_crest_item_in_db(sql_session, crest_item, region=region, item=item):
                MarketDay.create_from_crest_data(sql_session, crest_item, region=region, item=item, write=True)

    @staticmethod
    def update_market_order_data(sql_session, region):
        eve = CrestConnection()
        crest_items = MarketOrder.get_objects_from_crest(eve, region=region)
        for item in crest_items:
            i = True
            if Item.get_from_db_by_id(sql_session, item.type) is None:
                try:
                    i = Item.get_crest_item_by_attr(eve, 'id', item.type)
                    Item.create_from_crest_data(sql_session, i, write=True)
                    i = True
                except ValueError:
                    i = False
            if i:
                MarketOrder.create_from_crest_data(sql_session, item, write=True)
