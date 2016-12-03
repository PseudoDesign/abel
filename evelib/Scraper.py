from evelib.objects.MarketDay import MarketDay
from evelib.objects.MarketOrder import MarketOrder
from evelib.Crest import CrestConnection


class Scraper:
    @staticmethod
    def update_market_day_data(region, item):
        eve = CrestConnection()
        crest_items = MarketDay.get_objects_from_crest(eve, region=region, item=item).items
        for crest_item in crest_items:
            if not MarketDay.is_crest_item_in_db(crest_item, region=region, item=item):
                MarketDay.create_from_crest_data(crest_item, region=region, item=item, write=True)

    @staticmethod
    def update_market_order_data(region):
        eve = CrestConnection()
        crest_items = MarketOrder.get_objects_from_crest(eve, region=region)
        for item in crest_items:
            MarketOrder.create_from_crest_data(item, write=True)

