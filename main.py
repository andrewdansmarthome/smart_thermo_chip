import sys
from src.thermostat import Thermostat

# For dev mode, run with command: python3 main.py DEV
envMode = sys.argv[1]

print('current mode: ', envMode)
# Init thermostat
smartThermo = Thermostat()

# Run thermostat!
smartThermo.run()
