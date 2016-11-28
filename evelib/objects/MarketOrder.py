from sqlalchemy import DateTime, Column, Integer, BigInteger, Boolean, String, ForeignKey
from evelib.Sql import SqlBase
from sqlalchemy.orm import relationship
from evelib.objects.CrestSqlInterface import CrestSqlInterface


class MarketOrder(SqlBase, CrestSqlInterface):
    __tablename__ = "market_day"

    db_id = Column(BigInteger, primary_key=True)

    buy = Column(Boolean, nullable=False)
    issued = Column(DateTime, nullable=False)
    price = Column(Integer, nullable=False)
    volume = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    minVolume = Column(Integer, nullable=False)
    volumeEntered = Column(Integer, nullable=False)
    range = Column(String, nullable=False)

    crest_id = Column(BigInteger, nullable=False)

    station_id = Column(BigInteger, ForeignKey('station.id'), nullable=False)
    r_station = relationship("Station")

    item_id = Column(Integer, ForeignKey('item.id'), nullalbe=False)
    r_item = relationship("Item")
