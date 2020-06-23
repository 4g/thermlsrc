from ..services import *
from flask_restful import Resource, request
import logging
import random

class Sample(Resource):
    
    def __init__(self, **kwargs):
        self.service = Service()
        self.logger = logging.getLogger(__name__)
    
    def get(self):
        return [random.randrange(100,500, 20) for i in range(12)]
    
    def post(self):
        # import pdb;pdb.set_trace()
        self.logger.debug(request)
        self.service.write_point(request.get_json())
