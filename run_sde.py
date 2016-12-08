from evelib.objects.Station import Station
from evelib.Crest import CrestConnection
from evelib.Sql import SqlConnection
from evelib.Keys import Keys
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
        if Station.get_from_db_by_id(sql_connection.session, entry['stationID']) is None:
            Station.new_object_from_dict(sql_connection.session, eve, entry, write=True)


if __name__ == "__main__":
    keys = Keys()
    conn = "mysql+pymysql://sql_user:" + keys.sql_user + "@localhost/evedb"
    get_stations_from_yaml(sys.argv[1], conn)

