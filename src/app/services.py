from .daos import *
import logging
import csv
from dateutil.parser import parse
import pytz
import re


class Service:
    
    def __init__(self):
        self.influx_dao = InfluxDBDao()
        self.log = logging.getLogger(__name__)
        self.tz = pytz.timezone("Asia/Calcutta")
    
    def create_db(self, database_name):
        return self.influx_dao.create_database(database_name)
    
    def write_point(self, data):
        self.log.debug(f'Data in json: {data}')
        return self.influx_dao.write_point(point=data, database='YO')
    
    def bulk_write_points(self, request):
        
        request_obj = request.get_json()
        file_path = '/tmp/' + request_obj.get('file_name')
        self.log.info(f'Bulk inserting file content {file_path}')
        self.log.debug(f'Bulk inserting file content {file_path}')
        points = self.get_points_for_flat_file(file_path)
        self.influx_dao.bulk_write_points(points, 'YO', 'Flat')
    
    def get_points_for_normal_file(self, file_path):
        points = []
        with open(file_path) as csvfile:
            line_count = 0
            file_reader = csv.reader(csvfile, delimiter=',')
            tag = ''
            for row in file_reader:
                if line_count == 0:
                    tag = row[1]
                else:
                    raw_timestamp = row[0]
                    field_value = row[1]
                    original_timestamp = self.tz.localize(parse(raw_timestamp))
                    unix_timestamp = int(original_timestamp.timestamp() * 1000)
                    point = {}
                    point['tags'] = {
                        'Sensor': tag
                    }
                    point['fields'] = {
                        'Temperature': field_value
                    }
                    point['time'] = unix_timestamp
                    points.append(point)
                    self.log.info(f'Point {point}')
                    # self.log.debug(f'Processed {point}')
                
                line_count += 1
        
        self.log.info(f'Processed {line_count} rows')
        self.log.debug(f'Processed {line_count} rows')
        return points
    
    def get_points_for_flat_file(self, file_path):
        points = []
        with open(file_path) as csvfile:
            line_count = 0
            file_reader = csv.reader(csvfile, delimiter=',')
            tags = []
            for row in file_reader:
                if line_count == 0:
                    tags = row[1:]
                    tags = self.cleanup_tags(tags)
                    self.log.debug(f"Tags {tags}")
                    # import pdb;pdb.set_trace()
                else:
                    raw_timestamp = row[0]
                    tag_values = row[1:]
                    original_timestamp = self.tz.localize(parse(raw_timestamp))
                    unix_timestamp = int(original_timestamp.timestamp() * 1000)
                    point = {}
                    tags_dict = {}
                    # import pdb;pdb.set_trace()
                    for i in range(0, len(tags)):
                        if tags[i] and tag_values[i]:
                            tags_dict[tags[i]] = tag_values[i]
                    # import pdb;pdb.set_trace()
                    point['tags'] = tags_dict
                    point['fields'] = {"Test": 1}
                    point['time'] = unix_timestamp
                    points.append(point)
                    self.log.info(f'Point {point}')
                    # self.log.debug(f'Processed {point}')
                
                line_count += 1
        
        self.log.info(f'Processed {line_count} rows')
        self.log.debug(f'Processed {line_count} rows')
        return points
    
    def cleanup_tags(self, tags):
        modified_tags = []
        for tag in tags:
            modified_tags.append(re.sub("[/ ]", "_", tag.strip()))
        return modified_tags
