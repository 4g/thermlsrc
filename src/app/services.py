from .daos import *
import logging
import csv
from dateutil.parser import parse
class Service:

  def __init__(self):
    self.influx_dao = InfluxDBDao()
    self.log = logging.getLogger("Service")

  def create_db(self,database_name):
    return self.influx_dao.create_database(database_name)

  def write_point(self, data):
    self.log.error(f'Data in json: {data}')
    return self.influx_dao.write_point(point= data, database='YO')

  def bulk_write_points(self, request):

    request_obj = request.get_json()
    file_path = '/tmp/'+request_obj.get('file_name')
    self.log.info(f'Bulk inserting file content {file_path}')
    self.log.error(f'Bulk inserting file content {file_path}')
    points = []
    with open(file_path) as csvfile:
      line_count = 0
      file_reader = csv.reader(csvfile, delimiter=',')
      tag = ''
      for row in file_reader:
        if line_count == 0 :
          tag = row[1]
        else:
          raw_timestamp = row[0]
          field_value = row[1]
          original_timestamp = parse(raw_timestamp)
          unix_timestamp = int(original_timestamp.timestamp()*1000)
          point = {}
          point['tags'] = {
            'Sensor':tag
          }
          point['fields'] = {
            'Temperature':field_value
          }
          point['time'] = unix_timestamp
          points.append(point)
          self.log.info(f'Point {point}')
          # self.log.error(f'Processed {point}')

        line_count += 1

      self.log.info(f'Processed {line_count} rows')
      self.log.error(f'Processed {line_count} rows')
      self.influx_dao.bulk_write_points(points, 'YO', 'Temperature')