from flask import Blueprint, current_app

# data_transfer_bp = Blueprint('data_transfer_bp', __name__)
from ..services import *
import logging

# @data_transfer_bp.route('/insert',methods=('POST'))
# def test():
#   print(dir(current_app.config))
#   print(current_app.config)
#   create_db('YO')
#   return "Yo"
from flask_restful import Resource, request

class DataTransfer(Resource):
  def __init__(self):
    self.service = Service()
    self.log = logging.getLogger("gunicorn.debug")
  def get(self):
    self.service.create_db('New')
    return "Yo"

  def post(self):
    #import pdb;pdb.set_trace()
    self.log.debug(request)
    self.service.write_point(request.get_json())
