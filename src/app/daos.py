from .db import get_db_client

def create_database(database_name):
  influx_db_client = get_db_client()
  influx_db_client.create_database(database_name)