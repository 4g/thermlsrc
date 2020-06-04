from flask import Flask
from influxdb import InfluxDBClient

def create_app(config_file_name):
  app = Flask(__name__)
  app.config.from_object(config_file_name)
  from app.routes.data_transfer import data_transfer_bp
  app.register_blueprint(data_transfer_bp)
  
  return app

def create_influx_db_client(app):
  return InfluxDBClient(host=app.config.get('DATABASE_URL'), port=app.config.get('DATABASE_PORT'))