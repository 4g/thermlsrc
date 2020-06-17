from flask import g, current_app
from . import create_influx_db_client


def get_db_client():
    if not hasattr(g, 'influx_db_client'):
        g.influx_db_client = create_influx_db_client(current_app)
    return g.influx_db_client
