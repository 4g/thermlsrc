from ..services import *
import logging
from flask_restful import Resource, request


class BulkPointInsert(Resource):
    
    def __init__(self, **kwargs):
        self.service = Service()
        self.logger = kwargs.get('logger')
    
    def post(self):
        # import pdb;pdb.set_trace()
        self.logger.debug(request)
        self.service.bulk_write_points(request)
