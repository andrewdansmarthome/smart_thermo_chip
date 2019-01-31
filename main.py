import sys, threading
from src.thermostat import Thermostat

# For dev mode, run with command: python3 main.py DEV

# Init thermostat
smartThermo = Thermostat()

# Init threads
smartThermoThread = threading.Thread()

try:
  while True:
    print('What would you like to start? (a=all, t=thermostat): ')
    launch = input()
    if (launch == 't') or (launch == 'a'):
      smartThermoThread.start()
      smartThermoThread.run(smartThermo.run())
finally:
  if smartThermoThread.is_alive():
    smartThermoThread.exit()
  sys.exit(0)
