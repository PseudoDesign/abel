from sqlalchemy import DateTime, Column, Integer, Float, ForeignKey
from evelib.Sql import SqlBase
from sqlalchemy.orm import relationship
from evelib.objects.CrestSqlInterface import CrestSqlInterface
from datetime import datetime


class MarketDay(SqlBase, CrestSqlInterface):
    __tablename__ = "market_day"

    CREST_TIME_FORMAT = "%Y-%m-%dT00:00:00"

    id = Column(Integer, primary_key=True)

    volume = Column(Integer, nullable=False)
    orderCount = Column(Integer, nullable=False)
    lowPrice = Column(Float, nullable=False)
    highPrice = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)

    item_id = Column(Integer, ForeignKey('item.id'))
    r_item = relationship("Item")

    region_id = Column(Integer, ForeignKey('region.id'))
    r_region = relationship("Region")

    @classmethod
    def new_object_from_simple_crest(cls, crest):
        date = cls.string_to_datetime(getattr(crest, 'date'))
        setattr(crest, 'date', date)
        return super().new_object_from_simple_crest(crest)

    @classmethod
    def get_objects_from_crest(cls, crest_connection, **kwargs):
        if 'region' not in kwargs or 'item' not in kwargs:
            raise AttributeError()

        region_crest = kwargs['region'].get_crest_item_by_attr(crest_connection, 'id', kwargs['region'].id)
        item_crest = kwargs['item'].get_crest_item_by_attr(crest_connection, 'id', kwargs['item'].id, dereference=False)

        return region_crest().marketHistory(type=item_crest.href)

    @classmethod
    def date_to_string(cls, dt):
        # "2016-10-21T00:00:00"
        # Note that the time is always 00:00:00 eve time
        return dt.strftime(cls.CREST_TIME_FORMAT)

    @classmethod
    def string_to_datetime(cls, my_string):
        return datetime.strptime(my_string, cls.CREST_TIME_FORMAT)

