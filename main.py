import sys, threading
from src.thermostat import Thermostat
# import sys, socketio
# from env_setup import ENV_SERVER
from flask import Flask, Blueprint
from server.server import thermostat_server

app = Flask(__name__)
app.register_blueprint(thermostat_server)
@app.route('/')
def test():
  print('hit test route')
  return 'test service'

# For dev mode, run with command: python3 main.py DEV

# # Init socket client
# sio = socketio.Client()

# # Init websocket
# sio.connect(ENV_SERVER)
# print('socket connected with id: ', sio.sid)

# Init thermostat
smartThermo = Thermostat()

# Init threads
smartThermoThread = threading.Thread(target=smartThermo.run)

try:
  while True:
    print('What would you like to start? (a=all, t=thermostat): ')
    # launch = input()
    # if (launch == 't') or (launch == 'a'):
    # start thermostat controls in thread
    smartThermoThread.start()
    if __name__ == '__main__':
      # threading.Thread(target=app.run, kwargs={"debug": True}).start()
      app.run(debug=True)
    # smartThermo.run()
finally:
  if smartThermoThread.is_alive():
    smartThermoThread.exit()
  sys.exit(0)
