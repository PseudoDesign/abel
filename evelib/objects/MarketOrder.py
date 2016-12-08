from sqlalchemy import DateTime, Column, Integer, BigInteger, Boolean, String, ForeignKey, Float
from evelib.Sql import SqlBase
from sqlalchemy.orm import relationship
from evelib.objects.CrestSqlInterface import CrestSqlInterface
from sqlalchemy.dialects import sqlite
from evelib.objects.Station import Station
from datetime import datetime


class MarketOrder(SqlBase, CrestSqlInterface):
    __tablename__ = "market_order"

    # sqlite doesn't support BigInteger auto-increment primary keys.  Map it to Integer, just for testing
    BigInt = BigInteger().with_variant(sqlite.INTEGER(), 'sqlite')

    db_id = Column(BigInt, primary_key=True)

    buy = Column(Boolean, nullable=False)
    issued = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    minVolume = Column(Integer, nullable=False)
    volumeEntered = Column(Integer, nullable=False)
    range = Column(String(30, convert_unicode='force', unicode_error='backslashreplace'), nullable=False)

    id = Column(BigInteger, nullable=False)

    stationID = Column(BigInteger, ForeignKey('station.id'), nullable=False)
    r_station = relationship("Station")

    # item_id is "type" in this object
    type = Column(Integer, ForeignKey('item.id'), nullable=False)
    r_item = relationship("Item")

    capture_time = Column(DateTime, nullable=False)

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
        new_obj = super().new_object_from_crest(crest, **kwargs)
        new_obj.capture_time = datetime.now()
        return new_obj
