from sqlalchemy import String, Column, BigInteger, Integer, ForeignKey
from evelib.Sql import SqlBase
from sqlalchemy.orm import relationship
from evelib.Sql import SqlObjectInterface
from evelib.objects.SolarSystem import SolarSystem


class Station(SqlBase, SqlObjectInterface):
    __tablename__ = "station"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(128, unicode_error='backslashreplace'), nullable=False)

    solar_system_id = Column(Integer, ForeignKey('solar_system.id'), nullable=False)
    r_solar_system = relationship("SolarSystem")

    constellation_id = Column(Integer, ForeignKey('constellation.id'), nullable=False)
    r_constellation = relationship("Constellation")

    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    r_region = relationship("Region")

    @classmethod
    def create_new_object(cls, sql_session, crest_connection, id, name, solar_system_id, **kwargs):
        new_obj = cls(id=id, name=name)
        new_obj.solar_system_id = SolarSystem.get_from_db_or_crest_by_id(sql_session, crest_connection, solar_system_id).id
        if 'write' in kwargs:
            if kwargs['write']:
                new_obj.write_to_db(sql_session)
        return new_obj

    @classmethod
    def new_object_from_dict(cls, sql_session, crest_connection, entry, **kwargs):
        solar_system_id = SolarSystem.get_from_db_or_crest_by_id(
            sql_session, crest_connection, entry['solarSystemID']).id
        new_obj = cls(id=entry['stationID'],
                      name=entry['stationName'],
                      solar_system_id=solar_system_id,
                      constellation_id=entry['constellationID'],
                      region_id=entry['regionID'],
                      )
        if 'write' in kwargs:
            if kwargs['write']:
                new_obj.write_to_db(sql_session)
        return new_obj

    @classmethod
    def new_object_from_crest(cls, *args, **kwargs):
        raise NotImplementedError()
