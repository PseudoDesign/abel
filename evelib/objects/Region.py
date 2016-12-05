from sqlalchemy import String, Column, Integer
from evelib.Sql import SqlBase
from evelib.objects.CrestSqlInterface import CrestSqlInterface
from sqlalchemy.orm import relationship


class Region(SqlBase, CrestSqlInterface):
    __tablename__ = "region"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    r_constellations = relationship("Constellation")

    @classmethod
    def get_objects_from_crest(cls, crest_connection):
        return crest_connection.regions
