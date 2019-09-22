import sys, threading, requests
# from src.thermostat import Thermostat
from flask import Flask
app = Flask(__name__)

# For dev mode, run with command: python3 main.py DEV

# Init socket client
# sio = socketio.Client()

# Init websocket
# sio.connect(ENV_SERVER)
# print('socket connected with id: ', sio.sid)

# Init thermostat
# smartThermo = Thermostat()

class testThermo:
  def __init__(self):
    self.test = "testing"
  
  def run(self):
    requests.post('http://localhost:5000/power',json={})

# Init threads
# smartThermoThread = threading.Thread(None,smartThermo)
smartThermoThread = threading.Thread(target=testThermo)
appThread = threading.Thread(target=app)

try:
  while True:
    print('What would you like to start? (a=all, t=thermostat): ')
    launch = input()
    if (launch == 't') or (launch == 'a'):
      if __name__ == '__main__':
        smartThermoThread.start()
        appThread.start()
finally:
  if smartThermoThread.is_alive():
    smartThermoThread.exit()
    appThread.exit()
  sys.exit(0)
