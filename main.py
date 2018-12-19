import sys
from env.env import currentEnvURL
from src.thermostat import Thermostat

envMode = sys.argv[1]

smartThermo = Thermostat()

smartThermo.run()
