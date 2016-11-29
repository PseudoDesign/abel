from sqlalchemy import DateTime, Column, Integer, BigInteger, Boolean, String, ForeignKey, Float
from evelib.Sql import SqlBase
from sqlalchemy.orm import relationship
from evelib.objects.CrestSqlInterface import CrestSqlInterface


class MarketOrder(SqlBase, CrestSqlInterface):
    __tablename__ = "market_order"

    db_id = Column(Integer, primary_key=True)

    buy = Column(Boolean, nullable=False)
    issued = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    minVolume = Column(Integer, nullable=False)
    volumeEntered = Column(Integer, nullable=False)
    range = Column(String, nullable=False)

    id = Column(BigInteger, nullable=False)

    stationID = Column(BigInteger, ForeignKey('station.id'), nullable=False)
    r_station = relationship("Station")

    # item_id is "type" in this object
    type = Column(Integer, ForeignKey('item.id'), nullable=False)
    r_item = relationship("Item")

    @classmethod
    def get_objects_from_crest(cls, crest_connection, **kwargs):
        if 'region' not in kwargs:
            raise AttributeError()

        region_crest = kwargs['region'].get_crest_item_by_attr(crest_connection, 'id', kwargs['region'].id)
        return region_crest().marketOrdersAll().items

    @classmethod
    def new_object_from_crest(cls, crest, **kwargs):
        date = cls.string_to_datetime(getattr(crest, 'issued'))
        setattr(crest, 'issued', date)
        return super().new_object_from_crest(crest)
