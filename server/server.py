from flask import Flask, Blueprint

thermostat_server = Blueprint('thermostat_server', __name__)

@thermostat_server.route('/power', methods=['POST'])
def power():
  print('hit power api. switching:')
  return 'power'

@thermostat_server.route('/schedule', methods=['POST'])
def schedule():
  print('schedule api hit')
  return 'schedule'

@thermostat_server.route('/hold', methods=['POST'])
def hold(): 
  print('hold request hit:')
  return 'hold'
