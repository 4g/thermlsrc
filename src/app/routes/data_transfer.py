# from flask import current_app as app
from ..services import *
import logging
from flask_restful import Resource, request


class DataTransfer(Resource):

  def __init__(self, **kwargs):
    self.service = Service()
    self.logger = kwargs.get('logger')

  def get(self):
    self.service.create_db('New')
    return "Yo"

  def post(self):
    # import pdb;pdb.set_trace()
    self.logger.error(request)
    self.service.write_point(request.get_json())
