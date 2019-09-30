from flask import Flask, Blueprint
from server.server import thermostat_server

def create_app(smartThermo, furnace):
  app = Flask(__name__)
  app.register_blueprint(thermostat_server)
  app.config['smartThermo'] = smartThermo
  app.config['furnace'] = furnace

  return app
