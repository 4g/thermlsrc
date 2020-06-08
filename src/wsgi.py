from app import create_app
from config import DevConfig
import logging
application = create_app(DevConfig)

gunicorn_logger = logging.getLogger('gunicorn.debug')
application.logger.handlers = gunicorn_logger.handlers
application.logger.setLevel(gunicorn_logger.level)
