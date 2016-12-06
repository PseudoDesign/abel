from sqlalchemy import String, Column, Integer, ForeignKey
from evelib.Sql import SqlBase
from evelib.objects.CrestSqlInterface import CrestSqlInterface
from sqlalchemy.orm import relationship
from evelib.objects.Region import Region


class Constellation(SqlBase, CrestSqlInterface):
    __tablename__ = "constellation"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))

    r_solar_systems = relationship("SolarSystem")

    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    r_region = relationship("Region", back_populates="r_constellations")

    @classmethod
    def create_from_crest_data(cls, sql_session, crest_item, **kwargs):
        new_obj = cls.new_object_from_crest(crest_item)
        new_obj.region_id = Region.get_db_item_by_crest_item(sql_session,
            getattr(crest_item(), 'region')(), create_if_null=True, write=True).id
        if 'write' in kwargs:
            if kwargs['write']:
                new_obj.write_to_db(sql_session)
        return new_obj

    @classmethod
    def get_objects_from_crest(cls, crest_connection):
        return crest_connection.constellations().items

    @classmethod
    def get_crest_item_by_attr(cls, crest_connection, attr, value):
        crest_item = crest_connection.get_by_attr_value(cls.get_objects_from_crest(crest_connection), attr, value)
        return crest_item

    @classmethod
    def get_db_item_by_crest_item(cls, sql_session, crest_item, **kwargs):
        retval = cls.get_from_db_by_id(sql_session, crest_item.id)
        if retval is None:
            if 'create_if_null' in kwargs:
                if kwargs['create_if_null']:
                    retval = cls.create_from_crest_data(sql_session, crest_item, **kwargs)
        return retval

    @classmethod
    def get_and_create_all_in_region(cls, sql_session, region, **kwargs):
        constellations = region.constellations
        retval = []
        for c in constellations:
            retval += [cls.get_db_item_by_crest_item(sql_session, c, create_if_null=True, write=False)]
        return retval
