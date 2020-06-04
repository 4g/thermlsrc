from flask import Blueprint, current_app

# data_transfer_bp = Blueprint('data_transfer_bp', __name__)
from ..services import *
# @data_transfer_bp.route('/insert',methods=('POST'))
# def test():
#   print(dir(current_app.config))
#   print(current_app.config)
#   create_db('YO')
#   return "Yo"
from flask_restful import Resource
class DataTransfer(Resource):
  def get(self):
    create_db('New')
    return "Yo"