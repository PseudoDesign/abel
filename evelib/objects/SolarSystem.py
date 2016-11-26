from sqlalchemy import String, Column, Integer, ForeignKey
from evelib.Sql import SqlBase
from evelib.objects.Constellation import Constellation
from evelib.objects.CrestSqlInterface import CrestSqlInterface
from sqlalchemy.orm import relationship


class SolarSystem(SqlBase, CrestSqlInterface):
    __tablename__ = "solar_system"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    constellation_id = Column(Integer, ForeignKey('constellation.id'), nullable=False)
    r_constellation = relationship("Constellation")

    r_stations = relationship("Station")

    @classmethod
    def get_objects_from_crest(cls, crest_connection):
        return crest_connection.systems

    @classmethod
    def create_from_crest_data(cls, crest_item, **kwargs):
        new_obj = cls.new_object_from_simple_crest(crest_item)
        new_obj.constellation_id = Constellation.get_db_item_by_crest_item(
            getattr(crest_item(), 'constellation'), create_if_null=True, write=True).id
        if 'write' in kwargs:
            if kwargs['write']:
                new_obj.write_to_db()
        return new_obj
