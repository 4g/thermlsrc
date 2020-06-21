# from flask import current_app as app
from ..services import *
from flask_restful import Resource, request
import logging


class DataTransfer(Resource):
    
    def __init__(self, **kwargs):
        self.service = Service()
        self.logger = logging.getLogger(__name__)
    
    def get(self):
        self.service.create_db('New')
        # import pdb;
        # pdb.set_trace()
        self.logger.debug("Debug")
        self.logger.error("Error")
        self.logger.info("Info")
        return "Yo"
    
    def post(self):
        # import pdb;pdb.set_trace()
        self.logger.debug(request)
        self.service.write_point(request.get_json())
