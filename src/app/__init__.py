from flask import Flask, logging
from influxdb import InfluxDBClient
from flask_restful import Api, Resource
def create_app(config_file_name):
  app = Flask(__name__)
  api = Api(app)
  app.config.from_object(config_file_name)
  from app.routes.data_transfer import DataTransfer
  api.add_resource(DataTransfer, '/point/insert')
  
  return app

def create_influx_db_client(app):
  return InfluxDBClient(host=app.config.get('DATABASE_URL'), port=app.config.get('DATABASE_PORT'))


