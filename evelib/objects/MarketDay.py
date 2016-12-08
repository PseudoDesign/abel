from sqlalchemy import DateTime, Column, Integer, Float, ForeignKey
from evelib.Sql import SqlBase
from sqlalchemy.orm import relationship
from evelib.objects.CrestSqlInterface import CrestSqlInterface
from evelib.objects.DataSetInterface import DataSet, DataSetEntry


class MarketDay(SqlBase, CrestSqlInterface):
    __tablename__ = "market_day"

    CREST_TIME_FORMAT = "%Y-%m-%dT00:00:00"

    id = Column(Integer, primary_key=True)

    volume = Column(Integer, nullable=False)
    orderCount = Column(Integer, nullable=False)
    lowPrice = Column(Float, nullable=False)
    highPrice = Column(Float, nullable=False)
    avgPrice = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)

    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    r_item = relationship("Item")

    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    r_region = relationship("Region")

    @classmethod
    def crest_db_query(cls, sql_session, crest_item, **kwargs):
        if 'region' not in kwargs or 'item' not in kwargs:
            raise AttributeError()
        date = getattr(crest_item, 'date')
        if type(date) is str:
            date = cls.string_to_datetime(date)
        return cls.get_from_db_by_kwargs(
                sql_session,
                item_id=kwargs['item'].id,
                region_id=kwargs['region'].id,
                date=date)

    @classmethod
    def is_crest_item_in_db(cls, sql_session, crest_item, **kwargs):
        if cls.crest_db_query(sql_session, crest_item, **kwargs) is not None:
            return True
        return False

    @classmethod
    def new_object_from_crest(cls, crest, **kwargs):
        if 'region' not in kwargs or 'item' not in kwargs:
            raise AttributeError()
        date = cls.string_to_datetime(getattr(crest, 'date'))
        setattr(crest, 'date', date)
        new_obj = super().new_object_from_crest(crest)
        new_obj.region_id = kwargs['region'].id
        new_obj.item_id = kwargs['item'].id
        return new_obj

    @classmethod
    def get_objects_from_crest(cls, crest_connection, **kwargs):
        if 'region' not in kwargs or 'item' not in kwargs:
            raise AttributeError()

        region_crest = kwargs['region'].get_crest_item_by_attr(crest_connection, 'id', kwargs['region'].id)
        item_crest = kwargs['item'].get_crest_item_by_attr(crest_connection, 'id', kwargs['item'].id, dereference=False)

        return region_crest().marketHistory(type=item_crest.href)


class MarketDayDataSet(DataSet):

    TITLE = "Daily Market Data"

    region = None
    item = None

    def init_data_set_entries(self):
        self.x_data = DataSetEntry("Timestamp", "Time")
        self['volume'] = DataSetEntry("Volume", "Units")
        self['orderCount'] = DataSetEntry("Order Count", "Units")
        self['lowPrice'] = DataSetEntry("Low Price", "ISK")
        self['highPrice'] = DataSetEntry("High Price", "ISK")
        self['avgPrice'] = DataSetEntry("Average Price", "ISK")

    def get_title(self):
        return self.item.name + " " + self.TITLE + " in " + self.region.name

    @staticmethod
    def get_data_set(sql_session, region, item, **kwargs):
        retval = MarketDayDataSet()
        retval.region = region
        retval.item = item
        for entry in MarketDay.get_all_from_db_by_kwargs(sql_session, region_id=region.id, item_id=item.id):
            retval.add_db_obj(entry)
        return retval
