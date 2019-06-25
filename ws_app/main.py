# pylint: disable=C0103

"""Entrypoint of our server"""

import pathlib

import aiohttp.web

from routes import setup_routes
from utils import load_config
from views import setup_views

PROJECT_ROOT = pathlib.Path(__file__).parent

config = load_config("{}/config/config.yaml".format(PROJECT_ROOT))
config["PROJECT_ROOT"] = PROJECT_ROOT
config["STATIC_ROOT"] = "{}/static".format(PROJECT_ROOT)
config["DB_PATH"] = "{}/sensors.db".format(PROJECT_ROOT)
app = aiohttp.web.Application()
app.config = config
app.websockets = []

setup_routes(app)
app = setup_views(app)

aiohttp.web.run_app(app, host=config["HOST"], port=config["PORT"])
