from .db import get_db_client
from flask import json
import logging

class InfluxDBDao:
  influx_db_client = None

  def __init__(self):
    self.influx_db_client = get_db_client()
    self.logger = logging.getLogger("InfluxDbDao")

  def create_database(self, database_name):
    self.influx_db_client.create_database(database_name)

  def write_point(self, point, database, measurement='Test'):
    data = []
    if not point.get('Measurement'):
      point['measurement'] = measurement
    data.append(point)
    self.logger.error(f'DAO: {data}')
    self.influx_db_client.write_points(points=data, database=database)
