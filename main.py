import sys, socketio
from env_setup import ENV_SERVER
from src.thermostat import Thermostat

# For dev mode, run with command: python3 main.py DEV

# Init socket client
sio = socketio.Client()

# Init websocket
sio.connect(ENV_SERVER)
print('socket connected with id: ', sio.sid)

# Init thermostat
smartThermo = Thermostat()

# Run thermostat!
smartThermo.run()
