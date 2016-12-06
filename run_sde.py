from evelib.objects.Station import Station
from evelib.Crest import CrestConnection
from evelib.Sql import SqlConnection
import yaml
import sys


def get_stations_from_yaml(file_name, db_location="sqlite:///:memory:"):
    sql_connection = SqlConnection(db_location)
    sql_connection.create_tables()
    sql_connection.start_connection()
    eve = CrestConnection()
    with open(file_name) as file:
        data = yaml.load(file)
    for entry in data:
        Station.new_object_from_dict(sql_connection.session, eve, entry, write=True)


if __name__ == "__main__":
    get_stations_from_yaml(sys.argv[1], sys.argv[2])
