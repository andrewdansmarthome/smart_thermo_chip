from flask import Flask, Blueprint
from src.thermostat import furnace
thermostat_server = Blueprint('thermostat_server', __name__)

@thermostat_server.route('/power', methods=['POST'])
def power():
  print('hit power api. switching:')
  furnace.toggleAuto()
  return 'power toggled'

@thermostat_server.route('/schedule', methods=['POST'])
def schedule():
  print('schedule api hit')
  return 'schedule'

@thermostat_server.route('/hold', methods=['POST'])
def hold(): 
  print('hold request hit:')
  return 'hold'

@thermostat_server.route('/shutdown', methods=['POST'])
def shutdown():
  print('hit shutdown api. Ending Thermo control')
  return 'Thermostat shut down'
