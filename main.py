import sys, threading
from src.thermostat import Thermostat
from src.pin_setup import PinSetup
from src.furnace import Furnace
from server import create_app

# For dev mode, run with command: python3 main.py DEV

print('init the thermostat')
pins = PinSetup()
furnace = Furnace(pins)
smartThermo = Thermostat(furnace, pins)

# Init thermo thread
smartThermoThread = threading.Thread(target=smartThermo.run) 

app = create_app(smartThermo, furnace)

try:
  # print('What would you like to start? (a=all, t=thermostat): ')
  # launch = input()
  # if (launch == 't') or (launch == 'a'):
  # start thermostat controls in thread
  print('is thread alive:', smartThermoThread.is_alive())
  if (not smartThermoThread.is_alive()):
    smartThermoThread.start()
    print('started thermostat thread')
  app.run(debug=True)
finally:
  if smartThermoThread.is_alive():
    # smartThermoThread.exit()
  sys.exit(0)
