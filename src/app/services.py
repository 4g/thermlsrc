from .daos import *
import logging
class Service:

  def __init__(self):
    self.influx_dao = InfluxDBDao()
    self.log = logging.getLogger("Service")

  def create_db(self,database_name):
    return self.influx_dao.create_database(database_name)

  def write_point(self, data):
    self.log.error(f'Data in json: {data}')
    return self.influx_dao.write_point(point= data, database='YO')